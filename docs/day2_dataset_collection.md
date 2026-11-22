# GeoPulse – Day 2: Retail Dataset Collection & Validation Report

## Document Information
- **Project Title:** GeoPulse: Hyper-Local Retail Mobility Analytics
- **Document Name:** Retail Dataset Sourcing, Ingestion & Validation Specification
- **Phase:** Week 1 – Data Sourcing & Collection (Day 2)
- **Role:** Data Associate L1 Intern (Data Analysis and Business Insights)
- **Status:** Dataset Downloaded, Validated, and Documented in `data/raw/`

---

## 1. Dataset Source and Licensing

### 1.1 Source Repository
- **Repository Name:** `FabricRetailSales`
- **Owner / Organization:** `EmpoweredAnalysts`
- **Repository URL:** [https://github.com/EmpoweredAnalysts/FabricRetailSales](https://github.com/EmpoweredAnalysts/FabricRetailSales)
- **Default Branch:** `main`

### 1.2 Synthetic Nature & Transparency
- The dataset is **explicitly synthetic**. It models 24 months of operational and sales performance for a mid-sized national retail chain (*Northstar Retail*) operating 40 stores.
- In accordance with GeoPulse governance guidelines:
  - This dataset is **clearly labeled as synthetic**.
  - It is **not** claimed or represented as empirical real-world sensor surveillance, transactional banking logs, or physical pedestrian tracking.

### 1.3 Licensing Information
- **License Type:** **MIT License**
- **Copyright:** Copyright (c) 2025 EmpoweredAnalysts
- **Permissions:** Grants permission free of charge to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the data and software, subject to retaining the copyright notice.
- **Warranty:** Provided "as is", without warranty of any kind.

---

## 2. Downloaded Files & Storage Location

The verified dataset files were downloaded directly from raw GitHub endpoints into the project's designated raw storage directory without modification.

- **Local Storage Directory:** `data/raw/`

| File Name | File Size (Bytes) | Source Endpoint | Status |
| :--- | :---: | :--- | :---: |
| `retail_sales_demo_data.csv` | 77,211 bytes | `https://raw.githubusercontent.com/EmpoweredAnalysts/FabricRetailSales/main/retail_sales_demo_data.csv` | **Preserved Raw** |
| `retail_sales_data_dictionary.csv` | 1,075 bytes | `https://raw.githubusercontent.com/EmpoweredAnalysts/FabricRetailSales/main/retail_sales_data_dictionary.csv` | **Preserved Raw** |

> **Data Preservation Protocol:**  
> The downloaded files are stored as immutable raw inputs in `data/raw/`. No transformations, imputations, filtering, or modifications have been applied to these original CSV files.

---

## 3. Dataset Structure and Technical Validation

The primary dataset (`data/raw/retail_sales_demo_data.csv`) was loaded and inspected using Pandas (`pandas 3.1.0`). The programmatic verification confirmed the following:

### 3.1 Dimensions & Cardinality
- **Total Rows:** **960** rows
- **Total Columns:** **18** columns
- **Unique Stores (`store_id`):** Exactly **40** stores (`store_id` values range from 1 to 40)
- **Observations per Store:** Exactly **24** monthly records per store (40 stores × 24 months = 960 total observations)
- **Duplicate Rows:** **0** duplicate rows (100% unique store-month records)

### 3.2 Temporal Coverage
- **Years Covered:** **2023** and **2024** (2 full calendar years)
  - Year 2023: Months 1 through 12 (12 months)
  - Year 2024: Months 1 through 12 (12 months)
- **Temporal Granularity:** Monthly store-level records (`month_index` 1 to 12).

### 3.3 Column Data Types & Missing Values Audit

| # | Column Name | Pandas Dtype | Non-Null Count | Missing Values (NaN) | Missing % |
| :---: | :--- | :---: | :---: | :---: | :---: |
| 1 | `store_id` | `int64` | 960 | 0 | 0.0% |
| 2 | `year` | `int64` | 960 | 0 | 0.0% |
| 3 | `month` | `int64` | 960 | 0 | 0.0% |
| 4 | `month_index` | `int64` | 960 | 0 | 0.0% |
| 5 | `is_holiday_month` | `int64` | 960 | 0 | 0.0% |
| 6 | `ad_spend` | `float64` | 955 | **5** | **0.52%** |
| 7 | `foot_traffic` | `int64` | 960 | 0 | 0.0% |
| 8 | `avg_price` | `float64` | 960 | 0 | 0.0% |
| 9 | `staff_count` | `int64` | 960 | 0 | 0.0% |
| 10 | `store_size_sqft` | `int64` | 960 | 0 | 0.0% |
| 11 | `promo_days` | `int64` | 960 | 0 | 0.0% |
| 12 | `competitors_within_3km` | `int64` | 960 | 0 | 0.0% |
| 13 | `inventory_fill_rate` | `float64` | 960 | 0 | 0.0% |
| 14 | `returns_rate` | `float64` | 960 | 0 | 0.0% |
| 15 | `local_income_index` | `float64` | 960 | 0 | 0.0% |
| 16 | `parking_spaces` | `int64` | 960 | 0 | 0.0% |
| 17 | `store_age_years` | `int64` | 960 | 0 | 0.0% |
| 18 | `monthly_sales` | `float64` | 960 | 0 | 0.0% |

**Validation Findings:**
1. Exactly **5 missing values** are present in `ad_spend` (representing store-months where digital advertising spend was unrecorded).
2. All remaining 17 columns have **0 missing values** (100% complete).
3. The dataset exhibits clean type consistency (12 integer columns, 6 float columns) and adheres to expected domain ranges (e.g. `inventory_fill_rate` and `returns_rate` bounded between 0 and 1).

---

## 4. Alignment with GeoPulse Day 1 Requirements

### 4.1 Available Fields
The collected retail dataset fulfills key foundational requirements identified during Day 1:
- **`store_id`:** Provides a consistent primary key across 40 store entities.
- **`monthly_sales`:** Supplies the commercial performance dependent metric.
- **`foot_traffic`:** Provides store footfall volume for traffic-to-revenue modeling.
- **`year`, `month`, `month_index`, `is_holiday_month`:** Enables seasonal and holiday surge tracking.
- **Operational & Competitive Context:** `store_size_sqft`, `staff_count`, `promo_days`, `competitors_within_3km`, and `parking_spaces` provide rich explanatory variables for store performance segmentation.

---

## 5. Dataset Limitations & Missing GeoPulse Requirements

While `retail_sales_demo_data.csv` provides a strong commercial and operational baseline, it lacks geospatial and high-frequency mobility attributes necessary for hyper-local mobility analytics:

| Missing Requirement | Description | Impact on GeoPulse Project |
| :--- | :--- | :--- |
| **Geospatial Coordinates** (`latitude`, `longitude`) | The dataset has store identifiers (1–40) but lacks GPS coordinates. | Spatial proximity, GIS mapping, and hyper-local catchment heatmaps cannot be constructed from this table alone. |
| **Micro-Market Cluster / Locality** | No neighborhood/zone names (e.g., Koramangala, Indiranagar, Whitefield). | Location-level aggregation relies purely on numeric store IDs rather than named urban zones. |
| **Hourly Mobility Activity** | Traffic observations are aggregated monthly (`foot_traffic`) rather than hourly (`00:00–23:00`). | Intraday peak mobility curves, morning vs. evening commute surges, and hourly staffing alignments cannot be directly observed. |
| **Customer Dwell Time** | No dwell duration metric (average minutes spent per visit). | Dwell-time versus basket-size correlation cannot be computed without supplementary mobility data. |
| **Transaction Count** | Individual transaction count is not recorded (only total `monthly_sales` and `avg_price`). | Direct conversion rate (`transactions / footfall`) must be estimated via estimated transactions (`monthly_sales / avg_price`). |

---

## 6. Future Plan: Synthetic Mobility Data Generation (Phase 2)

To bridge the gap between monthly store performance and hyper-local geospatial dynamics, a dedicated synthetic mobility dataset will be developed in a subsequent phase:

1. **Explicit Synthetic Designation:**
   - The mobility dataset will be generated programmatically and **strictly labeled as synthetic**.
   - No claim will be made that simulated mobility records represent real physical tracking.
2. **Geospatial Enrichment:**
   - Map each of the 40 stores (`store_id` 1–40) to realistic retail coordinates (`latitude`, `longitude`) across representative commercial retail hubs in Bengaluru.
3. **Hourly Mobility Simulation:**
   - Model synthetic hourly footfall distributions capturing realistic retail traffic behaviors (e.g., weekday evening peaks, weekend midday surges, category-specific dwell times).
4. **Relational Integration:**
   - The synthetic mobility table will link directly to `retail_sales_demo_data.csv` via `store_id` and temporal keys, creating a unified, validated analytical schema for EDA and dashboarding.
5. **Separation of Concerns:**
   - **No mobility data is generated on Day 2.** Data collection for Day 2 remains exclusively focused on acquiring, verifying, and preserving the verified retail foundation dataset.

---

## 7. Summary & Verification Checklist

- [x] Created directory `data/raw/`.
- [x] Downloaded `retail_sales_demo_data.csv` (77,211 bytes) from verified source.
- [x] Downloaded `retail_sales_data_dictionary.csv` (1,075 bytes) from verified source.
- [x] Programmatically validated dataset with Pandas (960 rows, 18 columns, 40 stores, 2023–2024 monthly records, 5 NaNs in `ad_spend`, 0 duplicates).
- [x] Preserved raw downloaded files intact in `data/raw/` without alterations.
- [x] Documented source, MIT license, schema, limitations, and future mobility roadmap.
- [x] Strictly avoided Git operations (no commits, pushes, or branch modifications).
