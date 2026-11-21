# GeoPulse – Day 1: Project Requirements & Data Fields Identification

## Document Overview
- **Project Title:** GeoPulse: Hyper-Local Retail Mobility Analytics
- **Document Name:** Project Requirements and Data Fields Identification Specification
- **Phase:** Week 1 – Planning, Scoping & Requirements Engineering (Day 1)
- **Role:** Data Associate L1 Intern (Data Analysis and Business Insights)
- **Status:** Requirements Identified; Data Schema Defined; Ready for Dataset Sourcing

---

## 1. Project Objectives, Scope & Expected Outcomes

### 1.1 Project Objectives
The primary objective of **GeoPulse: Hyper-Local Retail Mobility Analytics** is to examine the intersection of physical human mobility patterns and retail commercial performance across granular geographic micro-markets. 

Key objectives include:
1. **Analyze Footfall Dynamics:** Understand when, where, and how customer traffic moves through commercial corridors and store locations.
2. **Correlate Mobility with Retail Performance:** Determine how visitor footfall and dwell time translate into store sales, transactions, and conversion rates.
3. **Identify Peak Operating Windows:** Pinpoint peak hourly, daily, and weekend mobility clusters to optimize staffing, inventory, and promotional timing.
4. **Evaluate Location Attractiveness:** Provide empirical foundations for a Location Opportunity Scoring model to compare store performance and identify growth potential.
5. **Develop Stakeholder Dashboards:** Deliver clear, interactive visualization tools for retail strategists, store managers, and operational planners.

### 1.2 Project Scope
- **Geographic Granularity:** Hyper-local retail clusters (store level, neighborhood/corridor level, and coordinate level).
- **Temporal Granularity:** Hourly observations and daily aggregated business performance across standard operating periods.
- **Analytical Boundaries:** Descriptive, diagnostic, and exploratory data analysis (EDA), statistical distribution profiling, spatial grouping, and metric derivation.
- **Data Governance:** Ground truth retail transactions linked with validated location coordinates and carefully modeled mobility data.

### 1.3 Expected Deliverables & Outcomes
- **Requirements Specification:** Fully defined field dictionary and schema requirements (this document).
- **Integrated Dataset:** Harmonized tabular datasets connecting retail sales with mobility indicators.
- **Data Validation & Quality Reports:** Checks on data completeness, non-null integrity, and spatial-temporal consistency.
- **Exploratory Data Analysis Notebooks:** Detailed notebooks documenting patterns, distributions, correlations, and anomalies.
- **Business Insights & KPI Summary:** Actionable commercial insights translating mobility metrics into retail strategies.
- **Interactive GeoPulse Dashboard:** Streamlit-based interactive tool for hyper-local performance exploration.

---

## 2. Data Architecture & Integration Strategy

To analyze hyper-local retail mobility, data must be captured across two distinct yet interconnected domains:
1. **Retail Data:** Measures commercial, financial, and operational store performance.
2. **Mobility Data:** Measures physical movement, foot traffic volume, dwell time, and geospatial coordinates.

```
+-----------------------------------+       +------------------------------------+
|            RETAIL DATA            |       |           MOBILITY DATA            |
+-----------------------------------+       +------------------------------------+
| • Store ID (Primary Key)          |       | • Store ID / Linked Location ID    |
| • Store Name & Category           |  <->  | • Store Location (Zone/Cluster)    |
| • Date & Time                     |       | • Latitude & Longitude             |
| • Sales & Revenue                 |       | • Date & Time (Hourly Window)      |
| • Transactions & Order Volumes    |       | • Footfall & Dwell Time            |
+-----------------------------------+       +------------------------------------+
                                      \   /
                                       v v
                      +------------------------------------+
                      |    INTEGRATED ANALYTICAL ENGINE    |
                      +------------------------------------+
                      | • Conversion Rate (%)              |
                      | • Revenue per Footfall Visitor     |
                      | • Hourly Peak Traffic Index        |
                      | • Location Opportunity Score       |
                      +------------------------------------+
```

### Linkage Mechanism:
- Primary Linkage Key: `Store_ID` (unique identifier for each retail outlet).
- Secondary Linkage Keys: `Date` / `Timestamp` for temporal synchronization, and `Latitude` & `Longitude` for geospatial alignment.

---

## 3. Identification of Required Data Fields

The following fields have been identified as necessary to fulfill the analytical scope of the GeoPulse project:

### 3.1 Retail Data Fields

| # | Field Name | Data Type | Classification | Purpose & Business Value |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Store ID** | `String` / `Alphanumeric` | **Essential** | Unique identifier for each store outlet. Serves as the primary key to link transactional performance with spatial mobility data. |
| 2 | **Store Name** | `String` | **Optional** | Human-readable name or brand of the retail outlet (e.g., Urban Grocer, Denim Hub) used for dashboard display and reporting. |
| 3 | **Store Category / Sector** | `String` / `Categorical` | **Essential** | Classification of retail business (e.g., Grocery, Apparel, Electronics, Pharmacy, F&B). Crucial for benchmarking baseline conversion rates and average dwell expectations. |
| 4 | **Date and Time** | `Datetime` (`YYYY-MM-DD HH:MM:SS`) | **Essential** | Timestamp of retail transaction or daily business reporting window. Necessary for tracking daily revenue, weekend surges, and seasonality trends. |
| 5 | **Sales (Gross Sales / Revenue)** | `Float` / `Decimal` (Currency) | **Essential** | Total monetary value generated in a given time period (e.g., INR). Required to compute revenue per footfall, average basket value, and store profitability. |
| 6 | **Transactions** | `Integer` | **Essential** | Number of completed payment transactions / bills generated. Essential for calculating conversion rate (`Transactions / Footfall`) and transaction density. |
| 7 | **Average Order Value (AOV)** | `Float` / `Decimal` | **Optional** | Average spend per transaction (`Sales / Transactions`). Indicates customer spending capacity and purchasing behavior across locations. |
| 8 | **Discount / Promotion Flag** | `Boolean` / `Binary` (`0/1`) | **Optional** | Indicates whether special marketing discounts or promotional campaigns were active. Useful to separate organic mobility surges from discount-driven footfall. |
| 9 | **Store Area / Size (Sq. Ft.)** | `Float` | **Optional** | Physical footprint of the retail outlet. Enables normalization metrics such as Sales per Square Foot and Footfall Capacity Utilization. |

---

### 3.2 Mobility Data Fields

| # | Field Name | Data Type | Classification | Purpose & Business Value |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Store Location (Zone / Corridor)** | `String` / `Categorical` | **Essential** | Descriptive geographic cluster or commercial neighborhood (e.g., Koramangala, Indiranagar, Whitefield, HSR Layout). Enables comparative micro-market clustering. |
| 2 | **Latitude and Longitude** | `Float` (Decimal Degrees, e.g., `12.9716, 77.5946`) | **Essential** | Precise geospatial coordinates of the retail store or mobility sensor. Essential for geospatial mapping, distance calculations, proximity clustering, and GIS heatmaps. |
| 3 | **Observation Date and Time** | `Datetime` (`YYYY-MM-DD HH:MM:SS`) | **Essential** | Timestamp of mobility observation. Enables time-series alignment with retail transaction logs. |
| 4 | **Footfall (Traffic Volume / Visitor Count)** | `Integer` | **Essential** | Count of individual customer visits or detected pedestrian movements within the store's catchment radius. The core denominator for conversion analysis. |
| 5 | **Dwell Time** | `Float` (Minutes) | **Essential** | Average duration spent by visitors at or inside the retail location. Indicates engagement level, browsing depth, and potential friction/queuing bottlenecks. |
| 6 | **Hourly Activity (Hour of Day)** | `Integer` (`0` to `23`) | **Essential** | Hourly distribution of pedestrian traffic. Critical for identifying morning, afternoon, and evening peak mobility windows to align staffing and operating hours. |
| 7 | **Day of Week (Weekday vs Weekend)** | `String` / `Categorical` | **Essential** | Day indicator (Monday through Sunday) and weekend classification. Reveals leisure mobility surges versus weekday convenience shopping patterns. |
| 8 | **Catchment Radius / Distance (Meters)** | `Float` | **Optional** | The geographic influence zone around the retail outlet where mobility pings are captured (e.g., 50m, 100m, 500m). Clarifies the catchment boundaries. |
| 9 | **Repeat Visitor Rate (%)** | `Float` / `Percentage` | **Optional** | Estimated percentage of visitors who have visited the location previously. Reflects customer loyalty and residential proximity vs transient transit traffic. |

---

## 4. Classification: Essential vs. Optional Fields

To ensure a disciplined and progressive analytical rollout, the data fields are categorized into **Essential (Tier 1)** and **Optional / Value-Add (Tier 2)**:

```
+---------------------------------------------------------------------------------------+
|                                    DATA FIELDS MATRIX                                 |
+-----------------------------------+---------------------------------------------------+
| ESSENTIAL FIELDS (Tier 1)         | OPTIONAL / VALUE-ADD FIELDS (Tier 2)              |
| Minimum Viable Analysis           | Advanced Enrichment & Segmentation                |
+-----------------------------------+---------------------------------------------------+
| • Store ID                        | • Store Name / Branding Label                     |
| • Store Location (Zone/Cluster)   | • Store Area (Square Feet)                        |
| • Store Category / Sector         | • Average Order Value (AOV)                       |
| • Date and Time                   | • Discount / Promotion Flag                       |
| • Sales (Revenue)                 | • Catchment Radius (Meters)                       |
| • Transactions                    | • Repeat Visitor Rate (%)                         |
| • Latitude and Longitude          | • Device / Sensor Identifier                      |
| • Footfall                        | • Ambient / Contextual Factors (e.g., Weather)    |
| • Dwell Time                      |                                                   |
| • Hourly Activity (Hour of Day)   |                                                   |
| • Day of Week                     |                                                   |
+-----------------------------------+---------------------------------------------------+
```

### Rationale for Classification:
1. **Essential Fields:** Form the absolute minimum viable schema required to answer core project questions (What is the footfall? When is peak traffic? How much revenue was generated? What is the conversion efficiency per location?).
2. **Optional Fields:** Enrich the baseline analysis with granular operational context (e.g., evaluating whether larger stores convert better, or if promotions skewed dwell times). The absence of optional fields will not stall the primary analytical pipeline.

---

## 5. Analytical Metrics and Business KPIs Enabled

The identified fields directly empower Member 3 to engineer the following core retail mobility KPIs:

1. **Footfall-to-Sales Conversion Rate (%):**
   $$\text{Conversion Rate} = \left(\frac{\text{Transactions}}{\text{Footfall}}\right) \times 100$$
   *Purpose:* Measures the effectiveness of a store in turning pedestrian footfall into paying customers.

2. **Sales per Footfall (Revenue Yield per Visitor):**
   $$\text{Sales per Visitor} = \frac{\text{Total Sales Revenue}}{\text{Total Footfall}}$$
   *Purpose:* Quantifies the monetary value generated by each visitor entering the retail catchment.

3. **Hourly Mobility Density Index:**
   $$\text{Hourly Traffic Share} = \left(\frac{\text{Hourly Footfall}}{\text{Daily Total Footfall}}\right) \times 100$$
   *Purpose:* Identifies hyper-local peak traffic hours to inform dynamic staffing and promotional pushes.

4. **Dwell Time vs. Basket Size Relationship:**
   *Purpose:* Evaluates whether longer browsing time leads to higher transaction values or indicates service delays.

5. **Location Opportunity Score (Composite Index):**
   *Purpose:* Combines normalized Footfall, Sales Yield, Dwell Time, and Conversion Rate to rank retail locations on overall commercial vibrancy.

---

## 6. Project Requirements Needing Clarification

To ensure smooth progression and prevent architectural mismatches during subsequent data integration, the following points have been identified for clarification:

1. **Data Granularity & Time Intervals:**
   - *Question:* Will raw mobility and retail data be provided as individual transaction/ping logs, or pre-aggregated at hourly / daily levels?
   - *Impact:* Determines the aggregation pipeline needed during preprocessing.

2. **Footfall Attribution & Geofencing Radius:**
   - *Question:* What spatial threshold defines a "footfall visit" (e.g., pedestrian walking within 25 meters of the storefront vs. physically entering the store)?
   - *Impact:* Influences dwell time interpretations and conversion rate baselines.

3. **Timeframe & Temporal Scope:**
   - *Question:* What is the baseline duration of the target dataset (e.g., 30 days, 1 quarter, 1 year), and which calendar dates are covered?
   - *Impact:* Determines whether weekly seasonality, month-end spikes, or holiday trends can be reliably modeled.

4. **Linking Key Consistency:**
   - *Question:* Will the mobility dataset carry the explicit `Store_ID` directly, or will spatial matching (nearest neighbor via `Latitude` and `Longitude`) be required to link mobility points to stores?
   - *Impact:* Dictates whether a geospatial join (GeoPandas / Haversine distance) is required.

5. **Category Benchmarks & Expectations:**
   - *Question:* Are there predefined conversion benchmarks per sector (e.g., Grocery typically has >70% conversion, while Electronics or Luxury Apparel may have 15–25%)?
   - *Impact:* Informs how anomaly detection and outlier filtering should be configured.

---

## 7. Next Steps & Implementation Roadmap

| Sequence | Task / Milestone | Output / Deliverable | Status |
| :---: | :--- | :--- | :---: |
| **Step 1** | Project Requirements & Field Identification | `docs/day1_data_requirements.md` | **Completed** |
| **Step 2** | Retail Foundation Dataset Sourcing & Verification | Dataset schema verification and baseline inspection | Pending |
| **Step 3** | Synthetic Mobility Data Design & Generation | Controlled simulated mobility dataset with clear labeling | Pending |
| **Step 4** | Data Cleaning, Preprocessing & Quality Validation | Integrated analytical table and validation log | Pending |
| **Step 5** | Exploratory Data Analysis & Statistical Profiling | Comprehensive EDA notebook and visualizations | Pending |
| **Step 6** | KPI Computation & Location Opportunity Scoring | Business insight report & scoring model | Pending |
| **Step 7** | Interactive Streamlit Dashboard Development | Multi-page dashboard with maps, charts, and filters | Pending |
| **Step 8** | Final Presentation & Project Handover | Final report, slide deck, and code walkthrough | Pending |
