import pandas as pd
from typing import Optional
from sqlalchemy import text
from langchain_core.tools import tool
from .database import engine
from . import config

@tool
def query_sales(
    region: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> str:
    """
    Retrieve high-level sales performance metrics (total sales, profit, margin, and number of orders).
    Optionally filter by region, product category, or a date range (YYYYMMDD integer format).
    """
    query = """
    SELECT 
        ROUND(SUM(f.sales), 2) AS total_sales,
        ROUND(SUM(f.profit), 2) AS total_profit,
        ROUND((SUM(f.profit) / SUM(f.sales)) * 100, 2) AS profit_margin,
        COUNT(DISTINCT f.order_id) AS total_orders
    FROM fact_sales f
    JOIN dim_customer c ON f.customer_id = c.customer_id
    JOIN dim_product p ON f.product_id = p.product_id
    WHERE 1=1
    """
    params = {}
    
    if region:
        query += " AND c.region = :region"
        params["region"] = region
    if category:
        query += " AND p.category = :category"
        params["category"] = category
    if start_date:
        query += " AND f.order_date_id >= :start_date"
        params["start_date"] = int(start_date)
    if end_date:
        query += " AND f.order_date_id <= :end_date"
        params["end_date"] = int(end_date)
        
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), params).fetchone()
            
        if not result or result[0] is None:
            return "No sales data found for the given criteria."
            
        return (
            f"Total Sales: ${result[0]:,.2f}\n"
            f"Total Profit: ${result[1]:,.2f}\n"
            f"Profit Margin: {result[2]}%\n"
            f"Total Orders: {result[3]}"
        )
    except Exception as e:
        return f"Error executing query_sales tool: {str(e)}"

@tool
def category_analysis() -> str:
    """
    Analyze product profitability by category.
    Returns the category name, total sales, total profit, and profit margin.
    """
    query = """
    SELECT 
        p.category,
        ROUND(SUM(f.sales), 2) AS total_sales,
        ROUND(SUM(f.profit), 2) AS total_profit,
        ROUND((SUM(f.profit) / SUM(f.sales)) * 100, 2) AS profit_margin
    FROM fact_sales f
    JOIN dim_product p ON f.product_id = p.product_id
    GROUP BY p.category
    ORDER BY total_profit DESC
    """
    try:
        with engine.connect() as conn:
            results = conn.execute(text(query)).fetchall()
            
        output = "Category Analysis:\n"
        for row in results:
            output += f"- {row[0]}: Sales: ${row[1]:,.2f} | Profit: ${row[2]:,.2f} | Margin: {row[3]}%\n"
        return output
    except Exception as e:
        return f"Error executing category_analysis tool: {str(e)}"

@tool
def regional_analysis() -> str:
    """
    Compare performance across geographic regions.
    Returns the region name, total sales, total profit, and profit margin.
    """
    query = """
    SELECT 
        c.region,
        ROUND(SUM(f.sales), 2) AS total_sales,
        ROUND(SUM(f.profit), 2) AS total_profit,
        ROUND((SUM(f.profit) / SUM(f.sales)) * 100, 2) AS profit_margin
    FROM fact_sales f
    JOIN dim_customer c ON f.customer_id = c.customer_id
    GROUP BY c.region
    ORDER BY total_sales DESC
    """
    try:
        with engine.connect() as conn:
            results = conn.execute(text(query)).fetchall()
            
        output = "Regional Analysis:\n"
        for row in results:
            output += f"- {row[0]}: Sales: ${row[1]:,.2f} | Profit: ${row[2]:,.2f} | Margin: {row[3]}%\n"
        return output
    except Exception as e:
        return f"Error executing regional_analysis tool: {str(e)}"

@tool
def get_forecast(months_ahead: int) -> str:
    """
    Retrieve future expected sales from the XGBoost forecast model results.
    Provide the number of months ahead you want to retrieve predictions for (1 to 6).
    """
    try:
        df = pd.read_csv(config.FORECAST_CSV_PATH)
        # Filter for forecasted rows only
        forecasts = df[df["forecast_type"] == "forecast"].head(months_ahead)
        
        if forecasts.empty:
            return "No forecast data currently available."
            
        output = "Forecasted Sales:\n"
        for _, row in forecasts.iterrows():
            output += f"- {row['date'][:7]}: Expected Revenue: ${row['predicted_revenue']:,.2f}\n"
        return output
    except Exception as e:
        return f"Error executing get_forecast tool: {str(e)}"

@tool
def business_insight(topic: str) -> str:
    """
    Generate business explanations and reasoning behind data trends. 
    Topics should be specific (e.g., 'Furniture', 'Central region', 'discounts').
    Provides qualitative insights derived from earlier historical EDA and loss analysis.
    """
    topic_lower = topic.lower()
    
    if "furniture" in topic_lower or "tables" in topic_lower or "bookcases" in topic_lower:
        return (
            "Furniture has significant revenue contribution but weaker profitability because: "
            "Tables and Bookcases create heavy losses, and high discounts heavily reduce margins."
        )
    elif "discount" in topic_lower:
        return (
            "Discounts above 25% consistently destroy profitability. Transactions with 36%+ discounts "
            "have negative average profit and a very high loss rate. Zero-discount transactions are the most reliably profitable."
        )
    elif "central" in topic_lower:
        return (
            "The Central region has the lowest profit margin among all regions. Losses in this region "
            "are heavily concentrated in the Furniture category (specifically Tables and Bookcases) driven by high discounts."
        )
    elif "copier" in topic_lower or "technology" in topic_lower:
        return (
            "Technology leads in profit despite not being the highest-revenue category. "
            "Copiers are the most profitable sub-category with low volume but extremely high margins."
        )
    else:
        return "I do not have pre-calculated qualitative insights on this specific topic. Please rely on the numerical tools for analysis."
