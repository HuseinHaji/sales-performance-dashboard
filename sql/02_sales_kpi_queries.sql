-- KPI queries for sales performance

SELECT SUM(revenue) AS total_revenue,
       SUM(profit) AS total_profit,
       AVG(margin) AS avg_margin
FROM fact_sales;

SELECT month_key,
       SUM(revenue) AS revenue,
       SUM(profit) AS profit
FROM fact_sales
GROUP BY month_key
ORDER BY month_key;

SELECT c.customer_name,
       SUM(f.revenue) AS revenue,
       SUM(f.profit) AS profit
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
GROUP BY c.customer_name
ORDER BY revenue DESC
LIMIT 10;
