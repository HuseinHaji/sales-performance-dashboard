-- Sales performance data model

CREATE TABLE dim_customer (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    region_id INTEGER NOT NULL,
    customer_segment TEXT NOT NULL
);

CREATE TABLE dim_product (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    product_category TEXT NOT NULL
);

CREATE TABLE dim_region (
    region_id SERIAL PRIMARY KEY,
    region_name TEXT NOT NULL
);

CREATE TABLE dim_channel (
    channel_id SERIAL PRIMARY KEY,
    channel_name TEXT NOT NULL
);

CREATE TABLE dim_date (
    month_key TEXT PRIMARY KEY,
    month_start DATE NOT NULL,
    month_label TEXT NOT NULL
);

CREATE TABLE fact_sales (
    sales_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL REFERENCES dim_customer(customer_id),
    product_id TEXT NOT NULL REFERENCES dim_product(product_id),
    region_id INTEGER NOT NULL REFERENCES dim_region(region_id),
    channel_id INTEGER NOT NULL REFERENCES dim_channel(channel_id),
    month_key TEXT NOT NULL REFERENCES dim_date(month_key),
    order_date DATE NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL,
    discount_rate NUMERIC(5,2) NOT NULL,
    revenue NUMERIC(12,2) NOT NULL,
    cost NUMERIC(12,2) NOT NULL,
    profit NUMERIC(12,2) NOT NULL,
    margin NUMERIC(5,2) NOT NULL
);

CREATE TABLE fact_targets (
    target_id SERIAL PRIMARY KEY,
    month_key TEXT NOT NULL REFERENCES dim_date(month_key),
    region_id INTEGER NOT NULL REFERENCES dim_region(region_id),
    sales_target NUMERIC(12,2) NOT NULL
);
