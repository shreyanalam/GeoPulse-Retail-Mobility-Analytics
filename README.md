# GeoPulse: Hyper-Local Retail Mobility Analytics

Hyper-Local Retail Mobility Analytics using Python and Geospatial Data.

---

> [!IMPORTANT]
> ### Synthetic Data Disclaimer
> The retail dataset utilized in this project is **fully synthetic demonstration data** sourced from the verified open-source repository [`EmpoweredAnalysts/FabricRetailSales`](https://github.com/EmpoweredAnalysts/FabricRetailSales) under the **MIT License**.
> - The dataset simulates monthly commercial and operational indicators for 40 retail stores over a 24-month horizon (2023–2024).
> - **This dataset does not represent actual, real-world customer observations, physical sensor pings, GPS surveillance, or private financial transactions.**
> - All analytical patterns, seasonal variations, correlations, and promotional responses reflect properties encoded in the synthetic simulation model and are intended strictly for educational, architectural, and data engineering workflow development.
> - **Correlation does not imply or establish causation:** Statistical associations observed in this synthetic data (e.g., between simulated foot traffic and sales) demonstrate co-occurrence within the model's generative rules, not empirical real-world causal mechanisms.

---

## Project Structure

```text
geopulse/
├── data/
│   └── raw/                                 # Immutable raw datasets
│       ├── retail_sales_demo_data.csv       # Sourced raw synthetic retail data (960 rows, 18 columns)
│       └── retail_sales_data_dictionary.csv # Data dictionary explaining fields
├── docs/                                    # Project documentation & milestone reports
│   ├── project_understand.md                # Day 1 project understanding
│   ├── day1_data_requirements.md            # Data requirements and schema specification
│   ├── day2_dataset_collection.md           # Dataset sourcing and validation report
│   ├── day3_python_pandas_setup.md          # Environment setup and initial verification
│   ├── day3_dataset_exploration.md          # EDA report on the synthetic retail dataset
│   └── individual_project_progress_report.md# Individual progress and development plan
├── notebooks/                               # Jupyter notebooks
│   ├── day3_pandas_practice.ipynb           # Preliminary Pandas methods practice
│   └── day3_dataset_exploration.ipynb       # Exploratory Data Analysis on synthetic dataset
└── outputs/
    └── eda/                                 # Generated exploratory visualization figures
        ├── monthly_sales_trend.png
        ├── monthly_foot_traffic_trend.png
        ├── top_bottom_stores_sales.png
        ├── foot_traffic_vs_monthly_sales.png
        ├── store_size_vs_sales.png
        └── promotion_holiday_analysis.png
```

---

## Project Objectives

1. **Retail Performance Profiling:** Explore commercial drivers, revenue density, and operational factors across store outlets using synthetic retail data.
2. **Geospatial & Mobility Enrichment (Upcoming Phase):** Design and integrate a separately labeled synthetic mobility dataset to simulate hyper-local foot traffic, geospatial coordinates, and customer dwell times across retail clusters.
3. **Data Quality & Hygiene:** Practice rigorous exploratory data analysis, outlier diagnostics, and data integrity preservation without mutating raw source files.
4. **Interactive Dashboarding:** Develop an intuitive visual interface to communicate business insights and location evaluation metrics.
