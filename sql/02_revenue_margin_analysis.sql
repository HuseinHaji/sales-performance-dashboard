-- Revenue and margin analysis by product category, customer segment, and channel.
WITH enriched_sales AS (
    SELECT
        st.transaction_id,
        st.channel,
        c.customer_segment,
        p.product_category,
        st.net_revenue,
        st.gross_margin,
        st.discount_rate,
        st.gross_revenue - st.net_revenue AS discount_amount
    FROM sales_transactions st
    JOIN customers c ON c.customer_id = st.customer_id
    JOIN products p ON p.product_id = st.product_id
    WHERE st.order_status IN ('Invoiced', 'Shipped')
)
SELECT
    product_category,
    customer_segment,
    channel,
    COUNT(DISTINCT transaction_id) AS order_count,
    SUM(net_revenue) AS net_revenue,
    SUM(gross_margin) AS gross_margin,
    SUM(gross_margin) / NULLIF(SUM(net_revenue), 0) AS gross_margin_pct,
    AVG(discount_rate) AS avg_discount_rate,
    SUM(discount_amount) AS discount_impact,
    SUM(net_revenue) / NULLIF(SUM(SUM(net_revenue)) OVER (), 0) AS revenue_contribution_share
FROM enriched_sales
GROUP BY product_category, customer_segment, channel
ORDER BY net_revenue DESC;
