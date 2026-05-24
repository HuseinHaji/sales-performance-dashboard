-- Regional and channel performance for management dashboarding.
WITH region_channel AS (
    SELECT
        c.region,
        c.country,
        st.channel,
        SUM(st.net_revenue) AS net_revenue,
        SUM(st.gross_margin) AS gross_margin,
        COUNT(DISTINCT st.transaction_id) AS order_count,
        COUNT(DISTINCT st.customer_id) AS active_customers
    FROM sales_transactions st
    JOIN customers c ON c.customer_id = st.customer_id
    WHERE st.order_status IN ('Invoiced', 'Shipped')
    GROUP BY 1, 2, 3
)
SELECT
    *,
    gross_margin / NULLIF(net_revenue, 0) AS gross_margin_pct,
    RANK() OVER (PARTITION BY region ORDER BY net_revenue DESC) AS channel_rank_in_region,
    net_revenue / NULLIF(SUM(net_revenue) OVER (PARTITION BY region), 0) AS region_channel_share
FROM region_channel
ORDER BY region, net_revenue DESC;
