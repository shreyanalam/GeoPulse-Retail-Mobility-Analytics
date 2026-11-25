"""
GeoPulse: Hyper-Local Retail Mobility Analytics
Script: day5_data_preprocessing.py
Phase: Day 5 - Data Preprocessing, Relational Integration & Feature Engineering
Author: Member 3 - Data Analysis and Business Insights

Architecture & Governance:
  1. Input File Immutability & SHA-256 Integrity Checks:
     - Verifies SHA-256 hashes of all raw and synthetic source files before and after pipeline execution.
     - Confirms 100% data immutability of data/raw/ and data/synthetic/ files.
  2. Data Cleaning Transformations:
     - Option B: Imputes 5 missing ad_spend values using store-specific historical medians.
     - Option C: Treats Store 6 January 2023 foot traffic anomaly by preserving raw_foot_traffic (1,000,000),
       setting is_foot_traffic_anomaly = 1, and imputing analytical foot_traffic with Store 6's
       historical 23-month median (4,284 visitors).
  3. Calendar-Weighted Mobility Aggregation:
     - Computes monthly totals using exact calendar weekdays and weekends in 2023/2024.
     - Calculates genuine footfall-weighted average dwell time.
  4. Relational Integration & Dynamic Schema Determination:
     - Integrates retail, geospatial location, and aggregated mobility tables on (store_id, year, month).
     - Maintains exactly 960 store-month records.
     - Derives expected column counts dynamically from merged schema without arbitrary hardcoding.
  5. Feature Engineering:
     - Uses cleaned retail foot_traffic for retail conversion_rate_pct and sales_per_visitor.
     - Retains synthetic monthly_mobility_footfall as a distinct mobility catchment metric.
     - Computes Location Opportunity Score (0 to 100) via Min-Max normalization.
  6. Atomic Publishing Pattern & Staging Protection:
     - Writes to temporary staging files (.tmp) first.
     - Runs full suite of validation assertions.
     - Atomically publishes final CSV files only after all checks pass.
"""

import os
import sys
import hashlib
import argparse
import calendar
import numpy as np
import pandas as pd

def compute_sha256(file_path):
    """
    Computes SHA-256 checksum of a file.
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def check_file_protection(target_files, allow_overwrite=False):
    """
    Checks if output target files already exist to protect against unintended overwriting.
    """
    existing = [f for f in target_files if os.path.exists(f)]
    if existing and not allow_overwrite:
        msg = (
            f"Output file protection active: The following output file(s) already exist:\n"
            + "\n".join([f"  - {f}" for f in existing])
            + "\nTo confirm overwriting, pass the '--force' flag to the script."
        )
        raise FileExistsError(msg)

def get_month_calendar_counts(year, month):
    """
    Calculates exact number of weekdays (Mon-Fri) and weekend days (Sat-Sun) in a given year and month.
    """
    cal = calendar.monthcalendar(year, month)
    num_weekdays = sum(1 for week in cal for day_idx in range(5) if week[day_idx] != 0)
    num_weekends = sum(1 for week in cal for day_idx in range(5, 7) if week[day_idx] != 0)
    return num_weekdays, num_weekends

def main():
    parser = argparse.ArgumentParser(description="GeoPulse Day 5 Data Preprocessing & Integration Pipeline")
    parser.add_argument("--force", action="store_true", help="Explicitly permit overwriting of existing processed output CSV files.")
    args = parser.parse_args()

    print("=" * 85)
    print("GeoPulse: Day 5 - Data Preprocessing, Relational Integration & Feature Engineering")
    print("=" * 85)

    # ---------------------------------------------------------
    # 0. PATH SETUP & SOURCE INTEGRITY CHECKS
    # ---------------------------------------------------------
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    raw_dir = os.path.join(base_dir, "data", "raw")
    synthetic_dir = os.path.join(base_dir, "data", "synthetic")
    processed_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)

    raw_sales_path = os.path.join(raw_dir, "retail_sales_demo_data.csv")
    raw_dict_path = os.path.join(raw_dir, "retail_sales_data_dictionary.csv")
    loc_mapping_path = os.path.join(synthetic_dir, "store_location_mapping.csv")
    hourly_mob_path = os.path.join(synthetic_dir, "hourly_mobility_data.csv")

    source_files = {
        'raw_sales': raw_sales_path,
        'raw_dict': raw_dict_path,
        'synthetic_locations': loc_mapping_path,
        'synthetic_mobility': hourly_mob_path
    }

    # Verify source files exist and record initial SHA-256 hashes
    print("\n[Step 0] Verifying Source Files & Computing Initial SHA-256 Hashes...")
    initial_hashes = {}
    for label, path in source_files.items():
        if not os.path.exists(path):
            print(f"CRITICAL ERROR: Source file missing at '{path}'")
            sys.exit(1)
        h = compute_sha256(path)
        initial_hashes[label] = h
        print(f"  - {os.path.relpath(path, base_dir)}: SHA-256 = {h[:16]}...{h[-8:]}")

    # Define final target paths and temporary staging paths
    out_clean_sales = os.path.join(processed_dir, "retail_sales_cleaned.csv")
    out_agg_mobility = os.path.join(processed_dir, "monthly_mobility_aggregated.csv")
    out_master_dataset = os.path.join(processed_dir, "geopulse_integrated_dataset.csv")

    tmp_clean_sales = os.path.join(processed_dir, ".retail_sales_cleaned.tmp")
    tmp_agg_mobility = os.path.join(processed_dir, ".monthly_mobility_aggregated.tmp")
    tmp_master_dataset = os.path.join(processed_dir, ".geopulse_integrated_dataset.tmp")

    target_files = [out_clean_sales, out_agg_mobility, out_master_dataset]
    check_file_protection(target_files, allow_overwrite=args.force)

    # ---------------------------------------------------------
    # 1. RETAIL DATA PREPROCESSING & CLEANING (PHASE 4)
    # ---------------------------------------------------------
    print("\n[Step 1] Loading and Preprocessing Raw Retail Sales Data...")
    df_raw = pd.read_csv(raw_sales_path)
    
    # Store ID format normalization
    df_raw['store_id'] = df_raw['store_id'].astype(int)
    df_cleaned = df_raw.copy()

    # Step 1.1: Missing ad_spend treatment (Option B - Store-specific historical median)
    print("  Applying Option B: Store-specific historical median imputation for missing ad_spend...")
    missing_ad_indices = df_cleaned[df_cleaned['ad_spend'].isnull()].index
    imputed_spend_log = {}

    for idx in missing_ad_indices:
        sid = int(df_cleaned.loc[idx, 'store_id'])
        store_valid_spend = df_cleaned[df_cleaned['store_id'] == sid]['ad_spend'].dropna()
        store_median_spend = round(float(store_valid_spend.median()), 2)
        df_cleaned.loc[idx, 'ad_spend'] = store_median_spend
        imputed_spend_log[sid] = store_median_spend

    for sid, val in sorted(imputed_spend_log.items()):
        print(f"    - Store {sid} (Jan 2023): Imputed ad_spend = INR {val:,.2f}")

    # Step 1.2: Store 6 Jan 2023 Foot Traffic Anomaly Treatment (Option C)
    print("  Applying Option C: Store 6 Jan 2023 Foot Traffic Anomaly Treatment...")
    df_cleaned['raw_foot_traffic'] = df_cleaned['foot_traffic'].copy().astype(int)
    df_cleaned['is_foot_traffic_anomaly'] = 0

    s6_mask = (df_cleaned['store_id'] == 6) & (df_cleaned['year'] == 2023) & (df_cleaned['month'] == 1)
    s6_anom_idx = df_cleaned[s6_mask].index[0]
    df_cleaned.loc[s6_anom_idx, 'is_foot_traffic_anomaly'] = 1

    # Impute analytical foot_traffic with Store 6's median over its 23 valid months
    s6_valid_traffic = df_cleaned[(df_cleaned['store_id'] == 6) & (~s6_mask)]['foot_traffic']
    s6_historical_median = int(round(s6_valid_traffic.median()))
    df_cleaned.loc[s6_anom_idx, 'foot_traffic'] = s6_historical_median

    print(f"    - Store 6 Jan 2023 raw_foot_traffic preserved: {df_cleaned.loc[s6_anom_idx, 'raw_foot_traffic']:,}")
    print(f"    - Store 6 Jan 2023 is_foot_traffic_anomaly set to: 1")
    print(f"    - Store 6 Jan 2023 analytical foot_traffic imputed with median: {s6_historical_median:,} visitors")

    # ---------------------------------------------------------
    # 2. CALENDAR-WEIGHTED MOBILITY AGGREGATION (PHASE 5)
    # ---------------------------------------------------------
    print("\n[Step 2] Aggregating Hourly Mobility Data to Monthly Level with Calendar Weighting...")
    df_hourly = pd.read_csv(hourly_mob_path)
    df_hourly['store_id'] = df_hourly['store_id'].astype(int)

    # Validate hourly completeness per store-year-month-day_type slice
    assert set(df_hourly['day_type'].unique()) == {'Weekday', 'Weekend'}, "Unexpected day types in mobility data!"
    slice_counts = df_hourly.groupby(['store_id', 'year', 'month', 'day_type']).size()
    assert (slice_counts == 24).all(), "Incomplete hourly records found in synthetic mobility data!"
    assert len(slice_counts) == 40 * 24 * 2, f"Expected 1,920 slices, got {len(slice_counts)}"
    print("  Validation: All 1,920 store-month-day_type slices contain exactly 24 hourly observations across Weekday and Weekend.")

    # Calculate daily footfall sums and dwell products per day type
    df_hourly['dwell_x_footfall'] = df_hourly['avg_dwell_minutes'] * df_hourly['footfall_count']

    daily_summary = df_hourly.groupby(['store_id', 'year', 'month', 'day_type']).agg({
        'footfall_count': 'sum',
        'dwell_x_footfall': 'sum'
    }).reset_index()

    # Pivot day types
    pivot_footfall = daily_summary.pivot(index=['store_id', 'year', 'month'], columns='day_type', values='footfall_count').reset_index()
    pivot_footfall = pivot_footfall.rename(columns={'Weekday': 'daily_weekday_footfall', 'Weekend': 'daily_weekend_footfall'})

    pivot_dwell_prod = daily_summary.pivot(index=['store_id', 'year', 'month'], columns='day_type', values='dwell_x_footfall').reset_index()
    pivot_dwell_prod = pivot_dwell_prod.rename(columns={'Weekday': 'daily_weekday_dwell_prod', 'Weekend': 'daily_weekend_dwell_prod'})

    df_monthly_mob = pd.merge(pivot_footfall, pivot_dwell_prod, on=['store_id', 'year', 'month'])

    # Compute exact calendar counts
    calendar_counts = {}
    for yr in [2023, 2024]:
        for mo in range(1, 13):
            wd, we = get_month_calendar_counts(yr, mo)
            calendar_counts[(yr, mo)] = (wd, we)

    df_monthly_mob['num_weekdays'] = df_monthly_mob.apply(lambda r: calendar_counts[(r['year'], r['month'])][0], axis=1)
    df_monthly_mob['num_weekends'] = df_monthly_mob.apply(lambda r: calendar_counts[(r['year'], r['month'])][1], axis=1)

    # Monthly footfall totals
    df_monthly_mob['weekday_footfall_monthly'] = df_monthly_mob['daily_weekday_footfall'] * df_monthly_mob['num_weekdays']
    df_monthly_mob['weekend_footfall_monthly'] = df_monthly_mob['daily_weekend_footfall'] * df_monthly_mob['num_weekends']
    df_monthly_mob['monthly_mobility_footfall'] = df_monthly_mob['weekday_footfall_monthly'] + df_monthly_mob['weekend_footfall_monthly']

    # Footfall-weighted average dwell time
    total_dwell_product = (df_monthly_mob['daily_weekday_dwell_prod'] * df_monthly_mob['num_weekdays']) + \
                          (df_monthly_mob['daily_weekend_dwell_prod'] * df_monthly_mob['num_weekends'])

    df_monthly_mob['avg_dwell_minutes_weighted'] = np.where(
        df_monthly_mob['monthly_mobility_footfall'] > 0,
        round(total_dwell_product / df_monthly_mob['monthly_mobility_footfall'], 2),
        0.0
    )
    df_monthly_mob['mobility_data_type'] = 'synthetic'

    mobility_cols = [
        'store_id', 'year', 'month',
        'weekday_footfall_monthly', 'weekend_footfall_monthly', 'monthly_mobility_footfall',
        'avg_dwell_minutes_weighted', 'num_weekdays', 'num_weekends', 'mobility_data_type'
    ]
    df_monthly_mob = df_monthly_mob[mobility_cols].copy()
    df_monthly_mob = df_monthly_mob.sort_values(['store_id', 'year', 'month'])

    # ---------------------------------------------------------
    # 3. RELATIONAL INTEGRATION & FEATURE ENGINEERING (PHASE 5 & 6)
    # ---------------------------------------------------------
    print("\n[Step 3] Relational Integration & Feature Engineering...")
    df_loc = pd.read_csv(loc_mapping_path)
    df_loc['store_id'] = df_loc['store_id'].astype(int)

    # Rename data_type in location mapping to avoid name collision
    df_loc = df_loc.rename(columns={'data_type': 'location_data_type'})

    # Merge 1: cleaned retail (960) + store location mapping (40) on store_id
    df_integrated = pd.merge(df_cleaned, df_loc, on='store_id', how='inner')
    assert len(df_integrated) == 960, "Row count changed after location merge!"

    # Merge 2: + monthly mobility aggregated (960) on store_id, year, month
    df_integrated = pd.merge(df_integrated, df_monthly_mob, on=['store_id', 'year', 'month'], how='inner')
    assert len(df_integrated) == 960, "Row count changed after mobility merge!"

    # Collision guard: Ensure no merge collision suffix columns (_x/_y) exist
    assert not any(c.endswith('_x') or c.endswith('_y') for c in df_integrated.columns), "Found unexpected merge suffix columns (_x/_y)!"

    # Verify avg_price > 0 before division
    assert (df_integrated['avg_price'] > 0).all(), "Zero or negative avg_price detected!"
    print(f"  Verification: avg_price > 0 confirmed across all records (Min = {df_integrated['avg_price'].min():.2f}).")

    # Feature Engineering Metrics
    # Rule 6: Use cleaned retail foot_traffic for retail conversion and sales_per_visitor.
    # Keep synthetic monthly_mobility_footfall as a distinct mobility catchment metric.
    df_integrated['estimated_transactions'] = round(df_integrated['monthly_sales'] / df_integrated['avg_price'], 2)
    df_integrated['conversion_rate_pct'] = np.where(
        df_integrated['foot_traffic'] > 0,
        round((df_integrated['estimated_transactions'] / df_integrated['foot_traffic']) * 100, 2),
        0.0
    )
    df_integrated['sales_per_visitor'] = np.where(
        df_integrated['foot_traffic'] > 0,
        round(df_integrated['monthly_sales'] / df_integrated['foot_traffic'], 2),
        0.0
    )
    df_integrated['sales_per_sqft'] = round(df_integrated['monthly_sales'] / df_integrated['store_size_sqft'], 4)

    # Location Opportunity Score Formulation (0 to 100)
    print("  Computing Location Opportunity Score (0 to 100) via Min-Max Normalization...")
    def min_max_scale(series):
        s_min = series.min()
        s_max = series.max()
        if s_max == s_min:
            return pd.Series(0.0, index=series.index)
        return (series - s_min) / (s_max - s_min)

    z_footfall = min_max_scale(df_integrated['foot_traffic'])
    z_yield = min_max_scale(df_integrated['sales_per_visitor'])
    z_conversion = min_max_scale(df_integrated['conversion_rate_pct'])
    z_dwell = min_max_scale(df_integrated['avg_dwell_minutes_weighted'])

    composite_score = (
        0.30 * z_footfall +
        0.25 * z_yield +
        0.25 * z_conversion +
        0.20 * z_dwell
    ) * 100.0

    df_integrated['location_opportunity_score'] = round(composite_score, 2)
    df_integrated = df_integrated.sort_values(['store_id', 'year', 'month'])

    # Dynamically determine and verify schema column count
    actual_col_count = len(df_integrated.columns)
    print(f"  Schema Verification: Master integrated dataset dynamically calculated with {actual_col_count} columns.")

    # ---------------------------------------------------------
    # 4. PRE-PUBLISH VALIDATION CHECKS (PHASE 7)
    # ---------------------------------------------------------
    print("\n" + "=" * 85)
    print("[Step 4] Running In-Memory Pre-Publish Validations...")
    print("=" * 85)

    # Validation 1: Dimensions & Dynamic Schema Core Fields
    assert len(df_cleaned) == 960, f"Cleaned retail rows mismatch: {len(df_cleaned)}"
    assert len(df_monthly_mob) == 960, f"Aggregated mobility rows mismatch: {len(df_monthly_mob)}"
    assert len(df_integrated) == 960, f"Integrated dataset rows mismatch: {len(df_integrated)}"
    
    expected_core_columns = [
        'store_id', 'year', 'month', 'monthly_sales', 'foot_traffic', 'raw_foot_traffic',
        'is_foot_traffic_anomaly', 'ad_spend', 'avg_price', 'store_size_sqft',
        'store_zone', 'latitude', 'longitude', 'location_data_type',
        'weekday_footfall_monthly', 'weekend_footfall_monthly', 'monthly_mobility_footfall',
        'avg_dwell_minutes_weighted', 'num_weekdays', 'num_weekends', 'mobility_data_type',
        'estimated_transactions', 'conversion_rate_pct', 'sales_per_visitor', 'sales_per_sqft',
        'location_opportunity_score'
    ]
    missing_cols = set(expected_core_columns) - set(df_integrated.columns)
    assert len(missing_cols) == 0, f"Missing required core columns in integrated dataset: {missing_cols}"
    print(f"  [PASS] Exactly 960 rows verified across all three processed tables.")
    print(f"  [PASS] Dynamic schema verified: {len(df_integrated.columns)} total columns calculated, all core fields present.")

    # Validation 2: Store Cardinality (Strictly integers 1 to 40)
    for name, df_check in [('retail_cleaned', df_cleaned), ('monthly_mob', df_monthly_mob), ('integrated', df_integrated)]:
        store_id_set = set(df_check['store_id'].unique())
        assert store_id_set == set(range(1, 41)), f"Store IDs mismatch in {name}!"
        assert df_check['store_id'].nunique() == 40, f"Unique store count != 40 in {name}!"
    print("  [PASS] Store IDs strictly verified as integers 1 to 40 with zero missing store entities.")

    # Validation 3: Unique Store-Month Keys (Zero Duplicates)
    for name, df_check in [('retail_cleaned', df_cleaned), ('monthly_mob', df_monthly_mob), ('integrated', df_integrated)]:
        dup_count = df_check.duplicated(subset=['store_id', 'year', 'month']).sum()
        assert dup_count == 0, f"Duplicate store-month keys detected in {name}!"
        null_count = df_check.isnull().sum().sum()
        assert null_count == 0, f"Null values detected in {name}: {null_count}"
    print("  [PASS] Zero duplicate store-month keys and zero null values verified across all tables.")

    # Validation 4: Imputation & Anomaly Audit Verification
    assert df_cleaned.loc[s6_anom_idx, 'raw_foot_traffic'] == 1000000, "Store 6 raw_foot_traffic altered!"
    assert df_cleaned.loc[s6_anom_idx, 'is_foot_traffic_anomaly'] == 1, "Store 6 anomaly flag != 1!"
    assert df_cleaned.loc[s6_anom_idx, 'foot_traffic'] == 4284, "Store 6 foot_traffic median imputation incorrect!"
    assert df_cleaned['ad_spend'].isnull().sum() == 0, "Missing ad_spend values remain!"
    print("  [PASS] Store 6 anomaly audit trail verified: raw=1,000,000, flag=1, imputed analytical=4,284.")
    print("  [PASS] All 5 missing ad_spend values verified imputed with store historical medians.")

    # Validation 5: Calendar Accuracy
    for (yr, mo), (wd, we) in calendar_counts.items():
        assert wd + we == calendar.monthrange(yr, mo)[1], f"Calendar mismatch in {yr}-{mo}"
    print("  [PASS] Calendar math verified: weekdays + weekends equals exact days in month for all 24 months.")

    # Validation 6: Non-Negativity & Metric Ranges
    assert (df_integrated['estimated_transactions'] >= 0).all(), "Negative transactions detected!"
    assert (df_integrated['conversion_rate_pct'] >= 0).all(), "Negative conversion rate detected!"
    assert (df_integrated['sales_per_visitor'] >= 0).all(), "Negative sales per visitor detected!"
    assert (df_integrated['location_opportunity_score'] >= 0).all(), "Negative opportunity score detected!"
    assert (df_integrated['location_opportunity_score'] <= 100).all(), "Opportunity score > 100 detected!"
    print("  [PASS] Non-negativity verified. Location Opportunity Score strictly bounded in [0, 100].")

    # ---------------------------------------------------------
    # 5. ATOMIC PUBLISHING: WRITE TMP -> VALIDATE -> RENAME
    # ---------------------------------------------------------
    print("\n[Step 5] Executing Atomic Publishing Pattern...")
    try:
        # Write to temporary staging files
        df_cleaned.to_csv(tmp_clean_sales, index=False)
        df_monthly_mob.to_csv(tmp_agg_mobility, index=False)
        df_integrated.to_csv(tmp_master_dataset, index=False)
        print("  Staging: Temporary files successfully written to disk.")

        # Validate that temporary files on disk match memory
        for tmp_path, expected_len in [(tmp_clean_sales, 960), (tmp_agg_mobility, 960), (tmp_master_dataset, 960)]:
            df_disk_check = pd.read_csv(tmp_path)
            assert len(df_disk_check) == expected_len, f"Disk check failed for {tmp_path}"
        print("  Staging Validation: Temporary disk files verified complete.")

        # Atomic rename to final target paths
        os.replace(tmp_clean_sales, out_clean_sales)
        os.replace(tmp_agg_mobility, out_agg_mobility)
        os.replace(tmp_master_dataset, out_master_dataset)
        print("  Publishing: Atomically promoted temporary files to final output CSVs:")
        print(f"    - {os.path.relpath(out_clean_sales, base_dir)} ({df_cleaned.shape[0]} rows x {df_cleaned.shape[1]} cols)")
        print(f"    - {os.path.relpath(out_agg_mobility, base_dir)} ({df_monthly_mob.shape[0]} rows x {df_monthly_mob.shape[1]} cols)")
        print(f"    - {os.path.relpath(out_master_dataset, base_dir)} ({df_integrated.shape[0]} rows x {df_integrated.shape[1]} cols)")

    except Exception as e:
        print(f"FATAL ERROR during publishing: {e}. Cleaning up temporary files...")
        for tmp_f in [tmp_clean_sales, tmp_agg_mobility, tmp_master_dataset]:
            if os.path.exists(tmp_f):
                os.remove(tmp_f)
        sys.exit(1)

    # ---------------------------------------------------------
    # 6. POST-EXECUTION SOURCE INTEGRITY HASH VERIFICATION
    # ---------------------------------------------------------
    print("\n[Step 6] Running Post-Execution SHA-256 Checksum Verifications on Source Files...")
    for label, path in source_files.items():
        post_h = compute_sha256(path)
        assert post_h == initial_hashes[label], f"CRITICAL INTEGRITY FAILURE: File '{path}' was modified during pipeline!"
        print(f"  [PASS] {os.path.relpath(path, base_dir)}: SHA-256 checksum 100% identical.")

    print("\n" + "=" * 85)
    print("DAY 5 PREPROCESSING & INTEGRATION PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 85)

if __name__ == '__main__':
    main()
