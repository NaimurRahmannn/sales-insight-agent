-- database/schema.sql

-- Drop tables if they exist to allow clean recreation
DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_date;

-- ==========================================
-- DIMENSIONS
-- ==========================================

CREATE TABLE dim_customer (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    segment VARCHAR(50),
    country VARCHAR(50),
    city VARCHAR(100),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    region VARCHAR(50)
);

CREATE TABLE dim_product (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(50),
    sub_category VARCHAR(50)
);

CREATE TABLE dim_date (
    date_id INT PRIMARY KEY, -- format: YYYYMMDD
    date DATE NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter INT NOT NULL
);

-- ==========================================
-- FACT TABLE
-- ==========================================

CREATE TABLE fact_sales (
    sale_id SERIAL PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    order_date_id INT NOT NULL,
    ship_date_id INT NOT NULL,
    customer_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    sales NUMERIC(12, 4) NOT NULL,
    quantity INT NOT NULL,
    discount NUMERIC(5, 2) NOT NULL,
    profit NUMERIC(12, 4) NOT NULL,
    profit_margin NUMERIC(8, 4),
    shipping_days INT,
    is_loss BOOLEAN NOT NULL,
    
    FOREIGN KEY (order_date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (ship_date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id)
);

-- ==========================================
-- INDEXES
-- ==========================================
-- Indexes are extremely useful in analytical (OLAP) databases because they significantly speed up:
-- 1. Joins: Filtering data in a fact table based on dimension attributes.
-- 2. Aggregations: AI Agent queries (e.g., GROUP BY region or category) execute much faster.

CREATE INDEX idx_fact_sales_order_date ON fact_sales(order_date_id);
CREATE INDEX idx_fact_sales_customer ON fact_sales(customer_id);
CREATE INDEX idx_fact_sales_product ON fact_sales(product_id);
-- The user requested a region index on fact_sales, but region is stored in dim_customer.
-- We index the region column in dim_customer to speed up filtering on region before joining.
CREATE INDEX idx_dim_customer_region ON dim_customer(region);

-- ==========================================
-- CHAT HISTORY
-- ==========================================

CREATE TABLE IF NOT EXISTS chat_sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_chat_sessions_id ON chat_sessions(session_id);
