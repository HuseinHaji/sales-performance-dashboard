-- Simple baseline forecast using a three-month moving average.
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', order_date)::date AS reporting_month,
        SUM(net_revenue) AS net_revenue,
        SUM(gross_margin) AS gross_margin
    FROM sales_transactions
    WHERE order_status IN ('Invoiced', 'Shipped')
    GROUP BY 1
),
forecast_base AS (
    SELECT
        reporting_month,
        net_revenue,
        AVG(net_revenue) OVER (ORDER BY reporting_month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS three_month_revenue_average,
        AVG(gross_margin) OVER (ORDER BY reporting_month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS three_month_margin_average
    FROM monthly
)
SELECT
    reporting_month + INTERVAL '1 month' AS forecast_month,
    'three_month_moving_average' AS forecast_method,
    three_month_revenue_average AS forecast_revenue,
    three_month_margin_average AS forecast_margin
FROM forecast_base
ORDER BY reporting_month DESC
LIMIT 1;
