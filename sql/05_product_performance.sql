-- Product performance using revenue, margin, volume, discount, and contribution share.
WITH product_sales AS (
    SELECT
        p.product_id,
        p.product_name,
        p.product_category,
        p.product_family,
        SUM(st.net_revenue) AS total_revenue,
        SUM(st.gross_margin) AS gross_margin,
        SUM(st.quantity) AS quantity_sold,
        COUNT(DISTINCT st.transaction_id) AS order_count,
        AVG(st.discount_rate) AS avg_discount_rate
    FROM sales_transactions st
    JOIN products p ON p.product_id = st.product_id
    WHERE st.order_status IN ('Invoiced', 'Shipped')
    GROUP BY 1, 2, 3, 4
)
SELECT
    *,
    gross_margin / NULLIF(total_revenue, 0) AS gross_margin_pct,
    total_revenue / NULLIF(SUM(total_revenue) OVER (), 0) AS revenue_share,
    CASE
        WHEN total_revenue / NULLIF(SUM(total_revenue) OVER (), 0) >= 0.10 THEN 'Revenue Drivers'
        WHEN gross_margin / NULLIF(total_revenue, 0) >= 0.52 THEN 'Margin Leaders'
        WHEN quantity_sold >= PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY quantity_sold) OVER () THEN 'Volume Products'
        WHEN avg_discount_rate >= 0.12 THEN 'Discount-Sensitive Products'
        ELSE 'Underperforming Products'
    END AS product_performance_band
FROM product_sales
ORDER BY total_revenue DESC;
