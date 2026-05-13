-- Dashboard views for sales monitoring

CREATE VIEW v_sales_summary AS
SELECT d.month_label,
       r.region_name,
       ch.channel_name,
       p.product_category,
       SUM(f.revenue) AS total_revenue,
       SUM(f.profit) AS total_profit,
       AVG(f.margin) AS avg_margin
FROM fact_sales f
JOIN dim_date d ON f.month_key = d.month_key
JOIN dim_region r ON f.region_id = r.region_id
JOIN dim_channel ch ON f.channel_id = ch.channel_id
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY d.month_label, r.region_name, ch.channel_name, p.product_category;
