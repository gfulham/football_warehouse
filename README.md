# NFL Fantasy Football Data Warehouse

## Overview
A personal data engineering project that integrates NFL fantasy projections, DraftKings salaries, betting odds, and stadium weather data into a Snowflake data warehouse. The project uses Python for data ingestion and processing, SQL and dbt for data transformation, and analytics models to support DFS lineup optimization and fantasy football decision-making.

## Tech Stack
- **Snowflake:** Cloud data warehouse and analytical SQL
- **Python:** Data ingestion, API integration, data cleaning, and processing
- **dbt:** Data transformation, modular modeling, and data quality testing
- **Pandas & NumPy:** Data manipulation and numerical analysis
- **Apache Airflow:** Workflow orchestration and scheduled pipeline execution

## Data Sources
- **Fantasy projections:** Player projections, floors, ceilings, and uncertainty metrics
- **DraftKings:** Player salaries and contest-related data
- **Betting odds:** NFL moneyline odds and implied market expectations
- **Weather:** Stadium-level forecasts, including temperature, precipitation, and wind

## Data Pipeline
1. **Ingestion:** Collect data from external APIs and CSV files using Python.
2. **Raw storage:** Load source data into Snowflake raw tables.
3. **Transformation:** Use dbt and SQL to clean, standardize, and join datasets.
4. **Analytics modeling:** Organize transformed data into staging, core, and mart layers.
5. **Downstream analytics:** Supply curated datasets to DFS lineup optimizers, player valuation models, and machine learning experiments.

## Related Projects
This warehouse serves as the foundation for separate fantasy football analytics and modeling projects, including DFS lineup optimization and reinforcement learning-based draft strategies.

## Goals
Demonstrate practical data engineering skills in cloud warehousing, ETL/ELT pipelines, data modeling, workflow orchestration, and analytics engineering through an end-to-end sports analytics use case.
