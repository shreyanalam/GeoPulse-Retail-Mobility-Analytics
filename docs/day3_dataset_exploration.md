# GeoPulse – Day 3: Dataset Exploration & Exploratory Data Analysis (EDA)

## Document Information
- **Project Title:** GeoPulse: Hyper-Local Retail Mobility Analytics
- **Document Name:** Retail Dataset Exploration & Exploratory Data Analysis (EDA) Report
- **Phase:** Week 1 – Implementation Phase 1 (Day 3)
- **Role:** Member 3 – Data Analysis and Business Insights
- **Status:** Exploratory Analysis Completed; Visualizations Generated; Data Governance & Synthetic Disclaimers Applied

---

> [!IMPORTANT]
> ### Mandatory Synthetic Data Disclaimer
> The retail dataset analyzed in this report is **fully synthetic demonstration data** sourced from the verified open-source repository [`EmpoweredAnalysts/FabricRetailSales`](https://github.com/EmpoweredAnalysts/FabricRetailSales) (MIT License).
> - The dataset models 24 months (2023–2024) of operational, marketing, and sales dynamics for 40 retail stores (960 store-month records).
> - **This dataset does not represent actual, real-world customer observations, physical sensor pings, GPS surveillance, or private financial transactions.**
> - All analytical patterns, seasonal variations, correlations, and promotional responses discussed in this report reflect properties encoded in the synthetic simulation model and are evaluated solely for educational, architectural, and data engineering workflow development.
> - **Correlation Does Not Establish Causation:** Any statistical association identified between variables (e.g., between simulated foot traffic and sales) represents mathematical co-occurrence within the synthetic data generation rules. It does not establish that foot traffic caused the sales lift without controlled causal experimentation.

---

## 1. Raw Dataset Integrity & Preservation Confirmation

- **Raw Files Verified in `data/raw/`:**
  1. `data/raw/retail_sales_demo_data.csv` (77,211 bytes)
  2. `data/raw/retail_sales_data_dictionary.csv` (1,075 bytes)
- **Raw Data Preservation Protocol:**
  - **No raw dataset values have been modified, deleted, imputed, or altered.**
  - **The Store 6 January 2023 foot traffic anomaly (1,000,000 visitors) is 100% preserved in `data/raw/retail_sales_demo_data.csv`.**
  - All exploratory data analysis, outlier scanning, and visualizations were conducted by loading the raw data into an analytical environment; no in-place modifications were written back to raw storage.

---

## 2. Dataset Overview & Structural Inspection

### 2.1 Dimensions and Architecture
- **Total Records:** **960** rows
- **Total Features:** **18** columns
- **Unique Store Outlets:** **40** stores (`store_id` 1 to 40)
- **Observations per Store:** Exactly **24** monthly records per store ($40 \times 24 = 960$)
- **Temporal Window:** **2023 – 2024** (24 consecutive calendar months, January 2023 through December 2024)
- **Data Granularity:** Store-month level (one aggregated observation per store per calendar month)

### 2.2 Feature Schema Breakdown
- **12 Integer Columns:** `store_id`, `year`, `month`, `month_index`, `is_holiday_month`, `foot_traffic`, `staff_count`, `store_size_sqft`, `promo_days`, `competitors_within_3km`, `parking_spaces`, `store_age_years`.
- **6 Float Columns:** `ad_spend`, `avg_price`, `inventory_fill_rate`, `returns_rate`, `local_income_index`, `monthly_sales`.

---

## 3. Data Quality Assessment Results

### 3.1 Missing Values & Duplicates
- **Duplicate Records:** **0 duplicate rows** (100% unique store-month records).
- **Missing Values Audit:**
  - `ad_spend`: **5 missing values** (NaNs), representing **0.52%** of the records.
  - All remaining 17 features: **0 missing values** (100% complete).
  - Total missing data points across the dataset: **5**.

### 3.2 Outlier Analysis & Critical Anomaly Identification
Statistical profiling using the Interquartile Range ($IQR = Q3 - Q1$) verified:

| Metric | Q1 (25%) | Q3 (75%) | IQR | Valid Range $[Q1 - 1.5 \times IQR, Q3 + 1.5 \times IQR]$ | Outlier Count | Outlier % |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `monthly_sales` | 2,553.87 | 3,904.91 | 1,351.04 | [527.31, 5,931.47] | 18 | 1.88% |
| `foot_traffic` | 3,960.50 | 5,001.50 | 1,041.00 | [2,399.00, 6,563.00] | 39 | 4.06% |
| `ad_spend` | 9,755.87 | 16,500.61 | 6,744.74 | [0.00, 26,617.71] | 30 | 3.14% |
| `store_size_sqft` | 23,620.50 | 30,500.75 | 6,880.25 | [13,300.12, 40,821.12] | 24 | 2.50% |
| `avg_price` | 19.55 | 24.66 | 5.12 | [11.87, 32.34] | 0 | 0.00% |

#### Critical Data Quality Finding (Preserved in Raw Data):
- **Store 6 Anomaly in `foot_traffic`:**  
  In **January 2023 (Month 1)**, `Store 6` recorded a foot traffic count of **1,000,000 visitors**, while its monthly sales revenue was recorded at **INR 4,517.63**.
  - Typical synthetic foot traffic across the entire chain ranges between 2,000 and 10,000 visitors per month.
  - This extreme recording represents a synthetic spike or intentional data artifact in the source dataset.
  - **Preservation Status:** This record remains intact in `data/raw/retail_sales_demo_data.csv`. For exploratory correlation analysis, the metric was evaluated both with and without this outlier to assess leverage.

---

## 4. Exploratory Data Analysis & Statistical Findings (from Synthetic Data)

All numerical results reported below have been directly verified by programmatic execution of the Jupyter notebook:

### 4.1 Foot Traffic vs. Monthly Sales Relationship (in Synthetic Data)
- **All 960 Records (with 1M outlier):** Pearson correlation $r = 0.0535$ (near zero due to extreme leverage of the Store 6 spike).
- **959 Records (excluding Store 6 1M outlier):** Pearson correlation **$r = 0.5969$ ($p < 0.001$)**.
- **Causation vs. Correlation Note:**  
  While this synthetic model exhibits a strong positive correlation between simulated visitor counts and sales revenue ($r = 0.5969$), **correlation does not establish causation**. In retail environments (and in this generative model), higher sales could result from confounding factors such as store size, local income levels, promotional activity, or seasonal demand rather than footfall alone.

### 4.2 Simulated Holiday Seasonality & Revenue Lift
Comparing simulated regular operating months with holiday months (November & December, where `is_holiday_month == 1`):
- **Regular Months (Jan – Oct, 800 observations):**
  - Mean Monthly Sales: **INR 3,213.04**
  - Mean Foot Traffic: **5,667.87 visitors**
- **Holiday Months (Nov – Dec, 160 observations):**
  - Mean Monthly Sales: **INR 3,897.96**
  - Mean Foot Traffic: **5,422.88 visitors**
- **Synthetic Finding:** Within the simulation model, holiday months yield a **+21.32% higher average monthly sales revenue** despite slightly lower average visitor counts, reflecting higher simulated basket values and holiday transaction sizes encoded in the synthetic dataset.

### 4.3 Store Performance Disparities (Top 5 vs. Bottom 5 in Synthetic Model)
Cumulative 24-month revenue reveals substantial variance across the 40 simulated store outlets:

| Store Group | Store ID | 24-Month Total Sales (INR) | Monthly Average Sales (INR) | Average Foot Traffic | Store Footprint (Sq. Ft.) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Top Store 1** | **Store 37** | **127,214.07** | **5,300.59** | 6,539.79 | 36,920 |
| **Top Store 2** | Store 12 | 120,444.64 | 5,018.53 | 5,232.42 | 34,228 |
| **Top Store 3** | Store 14 | 114,849.08 | 4,785.38 | 5,346.54 | 28,142 |
| **Top Store 4** | Store 22 | 113,822.80 | 4,742.62 | 5,321.17 | 37,921 |
| **Top Store 5** | Store 25 | 103,478.90 | 4,311.62 | 4,201.67 | 26,458 |
| *Bottom Store 5*| Store 15 | 60,126.61 | 2,505.28 | 4,499.71 | 22,112 |
| *Bottom Store 4*| Store 24 | 58,534.23 | 2,438.93 | 4,190.96 | 21,984 |
| *Bottom Store 3*| Store 35 | 51,856.25 | 2,160.68 | 5,507.17 | 23,450 |
| *Bottom Store 2*| Store 27 | 50,894.51 | 2,120.60 | 4,159.96 | 19,842 |
| **Bottom Store 1**| **Store 7** | **47,367.90** | **1,973.66** | 4,286.08 | 21,390 |

- **Performance Gap Ratio:** In this synthetic dataset, Store 37 outperforms Store 7 by **2.69x in total revenue**, reflecting simulated disparities in store footprint, demographic income indices, and traffic.

### 4.4 Store Size Efficiency & Sales Yield per Square Foot
- Store size ranges from **18,520 sq. ft.** to **45,448 sq. ft.** (mean: 27,659.60 sq. ft.).
- Correlation with sales in synthetic data: **$r = 0.2730$** (moderate positive).
- Sales per square foot metric ($\text{Sales} / \text{SqFt}$):
  - Mean: **0.125 INR / sq. ft.**
  - Range: **0.045 to 0.408 INR / sq. ft.**
- Larger simulated stores generally produce higher gross turnover, while compact formats exhibit higher revenue density per square foot.

### 4.5 Promotional Days Performance (in Synthetic Model)
- Promotional days range from 0 to 7 days per month (mean: 3.18 days).
- Correlation with sales in synthetic data: **$r = 0.1480$**.
- In the simulation, stores hosting 4–6 promotional days average 12–18% higher monthly sales than stores running 0–2 promotional days.

### 4.6 Operational Metrics: Inventory Fill Rate & Returns Rate
- **Inventory Fill Rate:** Averages **94.27%** across all synthetic records (range: 88.30% to 100.00%). Correlation with sales is weak ($r = -0.0640$), indicating inventory availability is uniformly high in the generator.
- **Customer Returns Rate:** Averages **3.72%** (range: 1.99% to 5.56%). Correlation with sales is mildly positive ($r = 0.1954$).

---

## 5. Visualizations Generated

All six charts in `outputs/eda/` were regenerated with explicit synthetic data designations, verified labels, units, and methodological notes:

| Visual Asset | File Path | Chart Title & Axis Labels | Analytical Focus |
| :--- | :--- | :--- | :--- |
| **1. Monthly Sales Trend** | [outputs/eda/monthly_sales_trend.png](file:///c:/Users/user/Documents/geopulse/outputs/eda/monthly_sales_trend.png) | **Title:** Monthly Total Sales Trend (2023 - 2024) [Synthetic Dataset]<br>**X-Axis:** Timeline (Year-Month)<br>**Y-Axis:** Total Monthly Sales (Thousands INR) | Shows 24-month network sales trajectory with simulated holiday surge bands (Nov–Dec). |
| **2. Monthly Foot Traffic Trend** | [outputs/eda/monthly_foot_traffic_trend.png](file:///c:/Users/user/Documents/geopulse/outputs/eda/monthly_foot_traffic_trend.png) | **Title:** Monthly Foot Traffic Volume Trend (2023 - 2024) [Synthetic Dataset]<br>**X-Axis:** Timeline (Year-Month)<br>**Y-Axis:** Total Monthly Foot Traffic (Thousands of Visitors) | Highlights pedestrian traffic timeline and annotates the preserved Store 6 Jan 2023 anomaly. |
| **3. Top vs. Bottom Stores** | [outputs/eda/top_bottom_stores_sales.png](file:///c:/Users/user/Documents/geopulse/outputs/eda/top_bottom_stores_sales.png) | **Title:** Top 5 vs Bottom 5 Stores by Total 24-Month Revenue [Synthetic Dataset]<br>**X-Axis:** Cumulative 24-Month Sales Revenue (Thousands INR)<br>**Y-Axis:** Store Identifier | Horizontal bar chart comparing revenue between top 5 and bottom 5 simulated stores. |
| **4. Traffic vs. Sales Correlation** | [outputs/eda/foot_traffic_vs_monthly_sales.png](file:///c:/Users/user/Documents/geopulse/outputs/eda/foot_traffic_vs_monthly_sales.png) | **Title:** Foot Traffic vs. Monthly Sales Revenue [Synthetic Dataset]<br>**X-Axis:** Monthly Foot Traffic (Visitors)<br>**Y-Axis:** Monthly Sales Revenue (INR) | Scatter plot with regression line ($r = 0.597$), noting that correlation does not establish causation. |
| **5. Store Size vs. Sales** | [outputs/eda/store_size_vs_sales.png](file:///c:/Users/user/Documents/geopulse/outputs/eda/store_size_vs_sales.png) | **Title:** Store Footprint (Sq. Ft.) vs. Monthly Sales Revenue [Synthetic Dataset]<br>**X-Axis:** Store Size (Square Feet)<br>**Y-Axis:** Monthly Sales Revenue (INR) | Evaluates physical store area vs. turnover, colored by simulated holiday season. |
| **6. Promotion & Holiday Analysis** | [outputs/eda/promotion_holiday_analysis.png](file:///c:/Users/user/Documents/geopulse/outputs/eda/promotion_holiday_analysis.png) | **Title:** Synthetic Promotional & Holiday Season Impact Analysis<br>**Subplot 1:** Sales Distribution by Holiday Status [Synthetic Data]<br>**Subplot 2:** Average Monthly Sales by Promotional Days [Synthetic Data] | Two-panel boxplot and barplot showing sales distribution across simulated promotional days and holidays. |

---

## 6. Notebook Execution & Verification

- **Notebook Path:** [notebooks/day3_dataset_exploration.ipynb](file:///c:/Users/user/Documents/geopulse/notebooks/day3_dataset_exploration.ipynb)
- **Cell Structure:** 20 total cells (8 Markdown cells, 12 Python code cells).
- **Execution Verification:**
  - All 12 code cells executed with sequential counts (1 through 12).
  - **Zero runtime or syntax errors.**
  - All outputs, tables, and charts are persisted directly in the notebook.
- **Safety Check:** The existing practice notebook `notebooks/day3_pandas_practice.ipynb` was untouched and preserved.

---

## 7. Dataset Limitations & Missing Mobility Requirements

While `retail_sales_demo_data.csv` provides a cohesive synthetic commercial baseline, it does not fulfill hyper-local geospatial mobility needs:

| Missing Field / Requirement | Current State in Synthetic Retail Data | Required Mobility Capability |
| :--- | :--- | :--- |
| **Geospatial Coordinates** (`latitude`, `longitude`) | Absent; stores only identified by integer IDs (1–40). | Required for map plotting, spatial radius queries, proximity clustering, and GIS heatmaps. |
| **Named Micro-Markets / Zones** | Absent; no locality names (e.g., Koramangala, Indiranagar). | Required for regional market segmentation and commercial cluster comparisons. |
| **Hourly Mobility Curves** | Traffic is aggregated monthly (`foot_traffic`). | Required to detect morning vs. evening commute spikes and intraday peak shopping windows. |
| **Dwell Time** | Absent; duration of customer stay is unrecorded. | Required to assess customer engagement depth, browsing behavior, and queuing bottlenecks. |
| **Discrete Transaction Count** | Absent; only total revenue and average price provided. | Direct conversion rate ($\text{Transactions} / \text{Footfall}$) must be estimated via $\text{Sales} / \text{Price}$. |

---

## 8. Summary of Data Governance Rules

1. **No Real-World Claims:** Simulated retail metrics must always be communicated as synthetic demonstration data.
2. **Correlation $\neq$ Causation:** Observed associations between variables describe model co-occurrences, not proven real-world cause-and-effect relationships.
3. **Data Immutability:** Raw CSV files in `data/raw/` remain pristine; all anomaly isolation is handled strictly in processing scripts without mutating raw records.
4. **Prerequisite for Day 4:** Day 4 will proceed only after formal approval and will focus on designing the synthetic mobility dataset architecture.
