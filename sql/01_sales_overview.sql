-- Monthly sales overview for a synthetic sales analytics prototype.
WITH closed_sales AS (
    SELECT
        DATE_TRUNC('month', order_date)::date AS reporting_month,
        transaction_id,
        customer_id,
        quantity,
        gross_revenue,
        net_revenue,
        gross_margin
    FROM sales_transactions
    WHERE order_status IN ('Invoiced', 'Shipped')
),
monthly_targets AS (
    SELECT
        month::date AS reporting_month,
        SUM(revenue_target) AS revenue_target
    FROM monthly_targets
    GROUP BY 1
)
SELECT
    s.reporting_month,
    SUM(s.gross_revenue) AS total_revenue,
    SUM(s.net_revenue) AS net_revenue,
    SUM(s.gross_margin) AS gross_margin,
    SUM(s.gross_margin) / NULLIF(SUM(s.net_revenue), 0) AS gross_margin_pct,
    COUNT(DISTINCT s.transaction_id) AS total_orders,
    SUM(s.quantity) AS total_quantity,
    COUNT(DISTINCT s.customer_id) AS active_customers,
    SUM(s.net_revenue) / NULLIF(COUNT(DISTINCT s.transaction_id), 0) AS avg_order_value,
    t.revenue_target,
    SUM(s.net_revenue) / NULLIF(t.revenue_target, 0) AS target_achievement_rate,
    SUM(s.net_revenue) / NULLIF(LAG(SUM(s.net_revenue)) OVER (ORDER BY s.reporting_month), 0) - 1 AS month_over_month_growth
FROM closed_sales s
LEFT JOIN monthly_targets t USING (reporting_month)
GROUP BY s.reporting_month, t.revenue_target
ORDER BY s.reporting_month;
