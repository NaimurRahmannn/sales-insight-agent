-- ====================================================================
-- database/example_queries.sql
-- Example Analytical Queries for the Sales Intelligence Database
-- These queries will later serve as the foundation for LangGraph tools.
-- ====================================================================

-- ---------------------------------------------------------
-- Query 1: Total sales and profit by region
-- ---------------------------------------------------------
SELECT 
    c.region,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    ROUND(SUM(f.profit) / SUM(f.sales) * 100, 2) AS profit_margin_pct
FROM 
    fact_sales f
JOIN 
    dim_customer c ON f.customer_id = c.customer_id
GROUP BY 
    c.region
ORDER BY 
    total_sales DESC;

-- ---------------------------------------------------------
-- Query 2: Most profitable categories
-- ---------------------------------------------------------
SELECT 
    p.category,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    ROUND(SUM(f.profit) / SUM(f.sales) * 100, 2) AS profit_margin_pct
FROM 
    fact_sales f
JOIN 
    dim_product p ON f.product_id = p.product_id
GROUP BY 
    p.category
ORDER BY 
    total_profit DESC;

-- ---------------------------------------------------------
-- Query 3: Loss-making subcategories
-- ---------------------------------------------------------
SELECT 
    p.category,
    p.sub_category,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit
FROM 
    fact_sales f
JOIN 
    dim_product p ON f.product_id = p.product_id
WHERE 
    f.is_loss = TRUE
GROUP BY 
    p.category, p.sub_category
HAVING 
    SUM(f.profit) < 0
ORDER BY 
    total_profit ASC; -- Lowest profit (biggest losses) first

-- ---------------------------------------------------------
-- Query 4: Monthly revenue trend
-- ---------------------------------------------------------
SELECT 
    d.year,
    d.month,
    d.month_name,
    ROUND(SUM(f.sales), 2) AS monthly_revenue
FROM 
    fact_sales f
JOIN 
    dim_date d ON f.order_date_id = d.date_id
GROUP BY 
    d.year, d.month, d.month_name
ORDER BY 
    d.year, d.month;

-- ---------------------------------------------------------
-- Query 5: Top customers by profit
-- ---------------------------------------------------------
SELECT 
    c.customer_name,
    c.segment,
    COUNT(DISTINCT f.order_id) AS total_orders,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit
FROM 
    fact_sales f
JOIN 
    dim_customer c ON f.customer_id = c.customer_id
GROUP BY 
    c.customer_id, c.customer_name, c.segment
ORDER BY 
    total_profit DESC
LIMIT 10;

-- ---------------------------------------------------------
-- Query 6: Discount impact on profitability
-- ---------------------------------------------------------
SELECT 
    CASE 
        WHEN discount = 0 THEN 'No Discount (0%)'
        WHEN discount > 0 AND discount <= 0.15 THEN 'Low (1-15%)'
        WHEN discount > 0.15 AND discount <= 0.25 THEN 'Medium (16-25%)'
        WHEN discount > 0.25 AND discount <= 0.35 THEN 'High (26-35%)'
        ELSE 'Very High (>35%)'
    END AS discount_tier,
    COUNT(*) AS transaction_count,
    ROUND(AVG(sales), 2) AS avg_sales,
    ROUND(AVG(profit), 2) AS avg_profit,
    ROUND(SUM(CASE WHEN is_loss THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS loss_rate_pct
FROM 
    fact_sales
GROUP BY 
    discount_tier
ORDER BY 
    avg_profit DESC;
