-- Customer performance, customer value bands, and revenue concentration.
WITH customer_sales AS (
    SELECT
        c.customer_id,
        c.customer_name,
        c.country,
        c.region,
        c.industry,
        c.customer_segment,
        SUM(st.net_revenue) AS total_revenue,
        SUM(st.gross_margin) AS gross_margin,
        COUNT(DISTINCT st.transaction_id) AS order_count,
        MAX(st.order_date) AS last_order_date
    FROM sales_transactions st
    JOIN customers c ON c.customer_id = st.customer_id
    WHERE st.order_status IN ('Invoiced', 'Shipped')
    GROUP BY 1, 2, 3, 4, 5, 6
),
ranked AS (
    SELECT
        *,
        gross_margin / NULLIF(total_revenue, 0) AS gross_margin_pct,
        total_revenue / NULLIF(order_count, 0) AS avg_order_value,
        DENSE_RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank,
        DENSE_RANK() OVER (ORDER BY gross_margin DESC) AS margin_rank,
        SUM(total_revenue) OVER (ORDER BY total_revenue DESC) / NULLIF(SUM(total_revenue) OVER (), 0) AS cumulative_revenue_share
    FROM customer_sales
)
SELECT
    *,
    CASE
        WHEN revenue_rank <= 10 AND gross_margin_pct >= 0.40 THEN 'Strategic Accounts'
        WHEN order_count >= 8 THEN 'Growth Accounts'
        WHEN order_count >= 5 THEN 'Stable Accounts'
        WHEN last_order_date < CURRENT_DATE - INTERVAL '120 days' THEN 'At-Risk / Declining Accounts'
        ELSE 'Low-Activity Accounts'
    END AS customer_value_band
FROM ranked
ORDER BY total_revenue DESC;
