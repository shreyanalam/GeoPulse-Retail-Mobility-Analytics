# GeoPulse – Day 4: Synthetic Mobility Data Generation & Validation Report

## Document Information
- **Project Title:** GeoPulse: Hyper-Local Retail Mobility Analytics
- **Document Name:** Synthetic Mobility Data Generation & Validation Specification
- **Phase:** Week 1 – Phase 2: Synthetic Mobility Modeling (Day 4)
- **Role:** Member 3 – Data Analysis and Business Insights
- **Status:** Synthetic Mobility Datasets Generated, Validated, and Documented

---

> [!IMPORTANT]
> ### Mandatory Synthetic Data Governance Notice
> The mobility datasets generated during Day 4 (`store_location_mapping.csv` and `hourly_mobility_data.csv`) are **mathematically simulated demonstration datasets**.
> - All geographic coordinates and hourly activity profiles are **explicitly labeled with `data_type = 'synthetic'`**.
> - **These records do not represent actual customer tracking, GPS traces, cellular pings, Wi-Fi sniffing, or physical camera counts.**
> - The synthetic mobility data provides representative hourly behavioral patterns designed specifically to enable spatial-temporal retail analytics, feature engineering, and dashboard prototyping for the GeoPulse project.

---

## 1. Objectives of Day 4

In the Day 3 Exploratory Data Analysis, critical gaps were identified in the raw commercial retail dataset (`retail_sales_demo_data.csv`):
1. **Absence of Geospatial Coordinates:** Stores were identified solely by integer IDs (`1` to `40`) without coordinates.
2. **Absence of Hourly Temporal Granularity:** Traffic was aggregated as a monthly total (`foot_traffic`), obscuring intraday morning, midday, and evening peak dynamics.
3. **Absence of Customer Dwell Time:** No duration metrics were available to model customer browsing depth and engagement.

**Day 4 Objectives Accomplished:**
- Generated simulated geographic locations for all 40 stores across 5 prominent commercial retail corridors in Bengaluru.
- Modeled realistic, reproducible diurnal footfall curves and customer dwell times across 40 stores, 24 months, weekdays/weekends, and 24 hourly intervals (46,080 records).
- Implemented output-file protection to prevent accidental overwriting without explicit authorization.
- Preserved both original raw CSV files in `data/raw/` in a 100% immutable state.

---

## 2. Methodology and Modeling Assumptions

### 2.1 Geographic Location Modeling
The 40 store entities from the foundational retail dataset were assigned to 5 recognized retail hubs in Bengaluru:

| Commercial Zone | Store IDs Assigned | Store Count | Center Latitude | Center Longitude | Simulated Coordinate Range |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Koramangala** | Stores 1 – 8 | 8 stores | 12.9352 | 77.6245 | Lat: [12.9298, 12.9406], Lon: [77.6190, 77.6299] |
| **Indiranagar** | Stores 9 – 16 | 8 stores | 12.9784 | 77.6408 | Lat: [12.9730, 12.9838], Lon: [77.6353, 77.6462] |
| **Whitefield** | Stores 17 – 24 | 8 stores | 12.9698 | 77.7500 | Lat: [12.9644, 12.9752], Lon: [77.7445, 77.7554] |
| **HSR Layout** | Stores 25 – 32 | 8 stores | 12.9116 | 77.6446 | Lat: [12.9062, 12.9170], Lon: [77.6391, 77.6500] |
| **Jayanagar** | Stores 33 – 40 | 8 stores | 12.9308 | 77.5838 | Lat: [12.9254, 12.9362], Lon: [77.5783, 77.5892] |

- **Geospatial Realism:** Each store coordinate was generated with a small uniform random jitter ($\pm 0.0055^\circ$, roughly 300m to 700m from the commercial cluster center) to simulate distinct physical retail addresses along major commercial thoroughfares.
- **Precision:** Coordinates are formatted to 6 decimal places (standard high-accuracy GPS standard).

---

### 2.2 Hourly Footfall Profile Generation
The hourly mobility simulator constructs representative hourly profiles across 4 dimensions:
$$\text{Total Records} = 40\text{ Stores} \times 24\text{ Months} \times 2\text{ Day Types (Weekday, Weekend)} \times 24\text{ Hours} = 46,080\text{ Rows}$$

#### Diurnal Activity Curves:
Normalized 24-hour weight vectors ($\sum w_h = 1.0$) were formulated to capture distinct weekday vs. weekend human movement:
1. **Closed & Night Hours (00:00 – 05:00):** Stores are closed. Footfall is near-zero (0 visitors, with occasional stochastic passerby of 1).
2. **Morning Opening & Commute (06:00 – 09:00):** Stores open around 08:30–09:30. Traffic climbs steadily from early commuters and morning shoppers.
3. **Midday & Lunch Window (10:00 – 13:00):** Sustained retail traffic. On weekdays, a noticeable lunch bump occurs between 12:00 and 13:30; on weekends, family and leisure shopping surges starting at 11:00.
4. **Afternoon Lull (14:00 – 16:00):** A slight dip in weekday shopping volume, whereas weekend leisure traffic remains elevated.
5. **Evening Prime Shopping Peak (17:00 – 20:00):**
   - **Weekday Peak:** Concentrated post-work commuter rush peaking at **19:00 (7:00 PM)** with highest footfall volume.
   - **Weekend Peak:** Broad, high-density leisure shopping and dining peak centered around **18:00 (6:00 PM)**.
6. **Closing Window (21:00 – 23:00):** Traffic tapers off sharply as retail outlets wind down operations.

#### Behavioral Lift Factors:
- **Weekend Volume Lift:** Weekend daily volume incorporates a **+35% multiplier** over weekdays, reflecting retail leisure surges.
- **Seasonal Holiday Lift:** In alignment with Day 3 EDA observations, November and December incorporate an **+18% holiday shopping multiplier**.
- **Store Footprint Capacity:** Baseline store traffic scales with physical store area (`store_size_sqft` from raw data), allowing larger flagship locations (e.g., 35,000+ sq. ft.) to support higher footfall capacity.

---

### 2.3 Dwell-Time Modeling Assumptions

> [!NOTE]
> **Key Architecture Rule on Dwell Time:**  
> The raw retail dataset (`retail_sales_demo_data.csv`) contains physical store area (`store_size_sqft`), but **does not contain a store category feature** (e.g., 'Apparel', 'Grocery').  
> Therefore, customer dwell time (`avg_dwell_minutes`) is mathematically parameterized based on **physical store footprint (`store_size_sqft`)**, hour of the day, day type (weekday vs. weekend), and seasonality (holiday months), and **not** on store category.

#### Dwell-Time Parameters:
- **Closed Hours (00:00 – 05:00):** Strictly $0.0$ minutes for zero-traffic hours (or $1.0 - 3.0$ minutes for isolated passersby).
- **Morning Quick Errands (06:00 – 09:00):** Fast transactional visits averaging $8.0 - 15.0$ minutes.
- **Daytime Shopping (10:00 – 16:00):** Standard browsing visits averaging $20.0 - 28.0$ minutes.
- **Evening Peak (17:00 – 20:00):** Extended dwell times averaging $32.0 - 44.0$ minutes as customers combine shopping with leisure and dining.
- **Weekend Leisure Effect:** Dwell times on weekends are modeled **$4.0 - 8.0$ minutes longer** than weekdays due to relaxed customer pacing.
- **Store Size Effect:** Larger stores (`store_size_sqft > 30,000`) add an additional $+0.0$ to $+4.5$ minutes of browsing time to account for larger floor area.
- **Non-Negativity Constraint:** Values are strictly non-negative floats rounded to 1 decimal place ($\min = 0.0$ min, $\max = 53.8$ min).

---

## 3. Generated Files & Storage Locations

All output files were generated by executing `scripts/generate_synthetic_mobility.py` with random seed `42`:

| Output File Path | Records | Columns | File Size | Description |
| :--- | :---: | :---: | :---: | :--- |
| [data/synthetic/store_location_mapping.csv](file:///c:/Users/user/Documents/geopulse/data/synthetic/store_location_mapping.csv) | **40** | **5** | 1,939 bytes | Simulated Bengaluru coordinates and zone mappings for all 40 stores. |
| [data/synthetic/hourly_mobility_data.csv](file:///c:/Users/user/Documents/geopulse/data/synthetic/hourly_mobility_data.csv) | **46,080** | **8** | 1,987,838 bytes | Synthetic 24-hour mobility and dwell-time profiles across 24 months. |
| [scripts/generate_synthetic_mobility.py](file:///c:/Users/user/Documents/geopulse/scripts/generate_synthetic_mobility.py) | — | — | 14,489 bytes | Standalone reproducible generation script with output-file protection. |

---

## 4. Column Schema Specifications

### 4.1 `store_location_mapping.csv`

| Column Name | Data Type | Range / Values | Description |
| :--- | :---: | :---: | :--- |
| `store_id` | Integer | `1` to `40` | Unique store identifier matching raw retail dataset primary key. |
| `store_zone` | String | 5 Zones | Designated commercial retail corridor in Bengaluru. |
| `latitude` | Float | `12.906598` to `12.979630` | Simulated latitude coordinate within Bengaluru city limits. |
| `longitude` | Float | `77.579114` to `77.754938` | Simulated longitude coordinate within Bengaluru city limits. |
| `data_type` | String | `'synthetic'` | Explicit governance label confirming simulated nature. |

### 4.2 `hourly_mobility_data.csv`

| Column Name | Data Type | Range / Values | Description |
| :--- | :---: | :---: | :--- |
| `store_id` | Integer | `1` to `40` | Foreign key referencing store outlet. |
| `year` | Integer | `2023`, `2024` | Calendar year of simulated observation. |
| `month` | Integer | `1` to `12` | Calendar month of observation. |
| `day_type` | String | `'Weekday'`, `'Weekend'` | Representative day category. |
| `hour` | Integer | `0` to `23` | Hour of the 24-hour day (`00:00` to `23:00`). |
| `footfall_count` | Integer | `0` to `32` | Representative hourly pedestrian visitor count ($\mu = 7.96$). |
| `avg_dwell_minutes` | Float | `0.0` to `53.8` | Estimated average minutes spent per visitor ($\mu = 19.98$). |
| `data_type` | String | `'synthetic'` | Explicit governance label confirming simulated nature. |

---

## 5. Technical Validation Results

All automated validation assertions were verified programmatically:

| Check # | Validation Parameter | Expected Value | Actual Result | Status |
| :---: | :--- | :---: | :---: | :---: |
| **1** | Location Record Count | Exactly 40 rows | **40 rows** | **PASS** |
| **2** | Unique Store IDs in Locations | Exactly integers 1 to 40 | **1 to 40 verified** | **PASS** |
| **3** | Stores per Zone Distribution | Exactly 8 stores per zone | **8 stores in each of the 5 zones** | **PASS** |
| **4** | Coordinate Range Bounds | Latitude: [12.8, 13.1]<br>Longitude: [77.5, 77.8] | **Lat: [12.9066, 12.9796]<br>Lon: [77.5791, 77.7549]** | **PASS** |
| **5** | Location Nulls & Duplicates | 0 nulls, 0 duplicates | **0 nulls, 0 duplicates** | **PASS** |
| **6** | Mobility Record Count | Exactly 46,080 rows | **46,080 rows** | **PASS** |
| **7** | Hourly Slice Completeness | Exactly 24 hours per slice (1,920 slices) | **100% of slices have exactly 24 records** | **PASS** |
| **8** | Non-Negativity Verification | `footfall_count >= 0`<br>`avg_dwell_minutes >= 0.0` | **Min footfall: 0<br>Min dwell: 0.0 min** | **PASS** |
| **9** | Mobility Nulls & Duplicates | 0 nulls, 0 duplicates | **0 nulls, 0 duplicates** | **PASS** |
| **10** | Weekday vs. Weekend Separation | Weekend footfall & dwell > Weekday | **Footfall: 9.14 vs. 6.78<br>Dwell: 21.8m vs. 18.1m** | **PASS** |
| **11** | Peak Activity Hours | Weekday: Evening commute<br>Weekend: Leisure evening | **Weekday: 19:00 (7 PM)<br>Weekend: 18:00 (6 PM)** | **PASS** |
| **12** | Output-File Protection | Halt if file exists without `--force` | **FileExistsError successfully raised** | **PASS** |
| **13** | Raw Data Preservation | Raw CSVs 100% immutable | **960 rows, 18 cols, Store 6 anomaly intact** | **PASS** |

---

## 6. Dataset Limitations & Separation of Concerns

1. **Synthetic Nature:** While parameters mirror authentic retail traffic behavior in Bengaluru, these records remain simulated models and must not be cited as empirical pedestrian surveillance.
2. **Aggregated Hourly Profiles:** Records represent typical hourly volume profiles for a representative weekday and weekend within each month, rather than continuous timestamped raw GPS pings.
3. **Data Independence (Unintegrated):** In strict compliance with Day 4 rules, **the retail and mobility datasets remain separate files and have NOT been integrated yet**.

---

## 7. Pending Day 5 Roadmap

1. **Data Preprocessing & Cleaning:**
   - Address the 5 missing values in `ad_spend` in `retail_sales_demo_data.csv`.
   - Implement outlier handling/capping strategy for the Store 6 January 2023 foot traffic anomaly.
2. **Multi-Table Relational Integration:**
   - Execute a clean relational join between commercial retail performance, geographic store coordinates, and hourly mobility profiles using `store_id`.
3. **Feature Engineering & Metric Alignment:**
   - Compute hyper-local conversion rates ($\text{Transactions} / \text{Footfall}$), revenue yield per visitor, and peak hourly mobility indices.
   - Aggregate hourly patterns to monthly summaries for location opportunity scoring.
