# PostgreSQL Analytics Database

This directory contains the data architecture layer for the AI-Powered Sales Intelligence Platform, transitioning flat CSV data into a robust **PostgreSQL Star Schema**.

## Purpose

The database layer serves as the single source of truth for downstream analytical applications, specifically:
- **LangGraph AI Agent:** Allows the agent to use SQL tools to query customer behaviors, profit trends, and loss makers dynamically.
- **Power BI / Streamlit:** Provides optimized analytical tables for fast dashboard rendering and aggregation.

## Architecture: Star Schema

The database relies on a centralized fact table connected to standardized dimensions.

### Fact Table
- `fact_sales`: Transactional records representing line items of an order. Contains all measurable KPIs (`sales`, `quantity`, `discount`, `profit`, `is_loss`) and foreign keys to all dimensions.

### Dimensions
- `dim_customer`: Customer demographics, segmentation, and geographic location.
- `dim_product`: Product hierarchies (category, sub-category) and names.
- `dim_date`: Time dimension used to aggregate data by year, quarter, month, and day without relying on complex SQL date functions.

## Setup Instructions

### 1. Requirements
- A running PostgreSQL instance. If you don't have one, run `docker-compose up -d` from the root directory to spin up a local instance.
- Python packages: `psycopg2-binary`, `sqlalchemy`, `python-dotenv`, `pandas`.

### 2. Environment Configuration
Create a `.env` file in the root directory (or ensure the existing one is configured):
```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=sales_intelligence
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

### 3. Initialize Database
Run the setup script from this directory to safely create the `sales_intelligence` database and initialize the star schema tables:
```bash
python database/create_database.py
```

### 4. ETL Load Data
Run the ETL script to transform `data/processed/cleaned_sales.csv` into dimensions and facts, and perform a fast batch insertion into PostgreSQL:
```bash
python database/load_data.py
```
*Note: The script automatically runs a validation suite at the end to confirm row counts and data integrity.*

## AI Agent Integration

Check `example_queries.sql` for the SQL blueprints that the LangGraph AI agent will use to answer business questions. The b-tree indexes defined in `schema.sql` are specifically optimized for these exact query patterns.
