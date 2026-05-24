-- Target achievement by month, region, product category, and sales rep.
WITH actuals AS (
    SELECT
        DATE_TRUNC('month', st.order_date)::date AS reporting_month,
        c.region,
        p.product_category,
        st.sales_rep_id,
        SUM(st.net_revenue) AS net_revenue,
        SUM(st.gross_margin) AS gross_margin,
        SUM(st.quantity) AS quantity_sold
    FROM sales_transactions st
    JOIN customers c ON c.customer_id = st.customer_id
    JOIN products p ON p.product_id = st.product_id
    WHERE st.order_status IN ('Invoiced', 'Shipped')
    GROUP BY 1, 2, 3, 4
)
SELECT
    a.reporting_month,
    a.region,
    a.product_category,
    sr.sales_rep_name,
    a.net_revenue,
    mt.revenue_target,
    a.net_revenue / NULLIF(mt.revenue_target, 0) AS revenue_target_achievement,
    a.gross_margin,
    mt.margin_target,
    a.gross_margin / NULLIF(mt.margin_target, 0) AS margin_target_achievement,
    a.quantity_sold,
    mt.volume_target,
    CASE
        WHEN a.net_revenue >= mt.revenue_target THEN 'Above Target'
        WHEN a.net_revenue >= mt.revenue_target * 0.95 THEN 'On Track'
        WHEN a.net_revenue >= mt.revenue_target * 0.85 THEN 'Below Target'
        ELSE 'Needs Attention'
    END AS target_status
FROM actuals a
JOIN monthly_targets mt
    ON mt.month::date = a.reporting_month
    AND mt.region = a.region
    AND mt.product_category = a.product_category
    AND mt.sales_rep_id = a.sales_rep_id
JOIN sales_reps sr ON sr.sales_rep_id = a.sales_rep_id
ORDER BY a.reporting_month, revenue_target_achievement DESC;
