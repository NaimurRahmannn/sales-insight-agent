import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join("..", ".env"))
load_dotenv(".env") # fallback

def get_db_engine():
    """Create SQLAlchemy engine using environment variables."""
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", "5432")
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "postgres")
    dbname = os.environ.get("POSTGRES_DB", "sales_intelligence")
    
    connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    return create_engine(connection_string)

def load_data():
    csv_path = os.path.join("..", "data", "processed", "cleaned_sales.csv")
    if not os.path.exists(csv_path):
        csv_path = os.path.join("data", "processed", "cleaned_sales.csv")
        
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path, parse_dates=["order_date", "ship_date"])
    
    engine = get_db_engine()
    
    print("1. Extracting and loading dim_customer...")
    dim_customer = df[[
        "customer_id", "customer_name", "segment", 
        "country", "city", "state", "postal_code", "region"
    ]].drop_duplicates(subset=["customer_id"])
    
    dim_customer.to_sql("dim_customer", engine, if_exists="append", index=False, method="multi", chunksize=1000)
    
    print("2. Extracting and loading dim_product...")
    dim_product = df[[
        "product_id", "product_name", "category", "sub_category"
    ]].drop_duplicates(subset=["product_id"])
    
    dim_product.to_sql("dim_product", engine, if_exists="append", index=False, method="multi", chunksize=1000)
    
    print("3. Extracting and loading dim_date...")
    # Get all unique dates from both order and ship dates
    unique_dates = pd.concat([df["order_date"], df["ship_date"]]).drop_duplicates().dropna()
    dim_date = pd.DataFrame({"date": unique_dates})
    
    # Generate integer date_id (YYYYMMDD)
    dim_date["date_id"] = dim_date["date"].dt.strftime("%Y%m%d").astype(int)
    dim_date["year"] = dim_date["date"].dt.year
    dim_date["month"] = dim_date["date"].dt.month
    dim_date["month_name"] = dim_date["date"].dt.strftime("%B")
    dim_date["quarter"] = dim_date["date"].dt.quarter
    
    # Ensure date_id is first column and sort
    dim_date = dim_date[["date_id", "date", "year", "month", "month_name", "quarter"]].sort_values("date_id")
    dim_date.to_sql("dim_date", engine, if_exists="append", index=False, method="multi", chunksize=1000)
    
    print("4. Preparing and loading fact_sales...")
    fact_sales = df.copy()
    
    # Map dates to integer date IDs
    fact_sales["order_date_id"] = fact_sales["order_date"].dt.strftime("%Y%m%d").astype(int)
    fact_sales["ship_date_id"] = fact_sales["ship_date"].dt.strftime("%Y%m%d").astype(int)
    
    # Select columns matching the PostgreSQL schema (exclude raw date timestamps and non-DB columns if any)
    fact_columns = [
        "order_id", "order_date_id", "ship_date_id", 
        "customer_id", "product_id", "sales", "quantity", 
        "discount", "profit", "profit_margin", "shipping_days", "is_loss"
    ]
    fact_sales = fact_sales[fact_columns]
    
    fact_sales.to_sql("fact_sales", engine, if_exists="append", index=False, method="multi", chunksize=1000)
    
    print("Data loading completed successfully!")
    return engine

def validate_data(engine):
    print("\n--- Running Validation Suite ---")
    queries = {
        "fact_sales count": "SELECT COUNT(*) FROM fact_sales",
        "dim_customer count": "SELECT COUNT(*) FROM dim_customer",
        "dim_product count": "SELECT COUNT(*) FROM dim_product",
        "dim_date count": "SELECT COUNT(*) FROM dim_date",
        "Orphaned orders (NULL customer)": "SELECT COUNT(*) FROM fact_sales WHERE customer_id IS NULL",
        "Orphaned orders (NULL product)": "SELECT COUNT(*) FROM fact_sales WHERE product_id IS NULL"
    }
    
    with engine.connect() as conn:
        for name, query in queries.items():
            result = conn.execute(text(query)).scalar()
            print(f"{name}: {result}")
            
if __name__ == "__main__":
    db_engine = load_data()
    validate_data(db_engine)
