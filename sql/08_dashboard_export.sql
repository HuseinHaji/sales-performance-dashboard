-- Dashboard export base table: transaction grain enriched with dimensions and targets.
SELECT
    st.transaction_id,
    DATE_TRUNC('month', st.order_date)::date AS reporting_month,
    st.order_date,
    st.invoice_date,
    c.customer_id,
    c.customer_name,
    c.country,
    c.region,
    c.industry,
    c.customer_segment,
    p.product_id,
    p.product_name,
    p.product_category,
    p.product_family,
    sr.sales_rep_id,
    sr.sales_rep_name,
    sr.team,
    sr.manager,
    st.channel,
    st.order_status,
    st.quantity,
    st.unit_price,
    st.discount_rate,
    st.gross_revenue - st.net_revenue AS discount_amount,
    st.gross_revenue,
    st.net_revenue,
    st.cost,
    st.gross_margin,
    st.gross_margin / NULLIF(st.net_revenue, 0) AS gross_margin_pct,
    mt.revenue_target,
    mt.margin_target,
    mt.volume_target,
    st.net_revenue / NULLIF(mt.revenue_target, 0) AS target_achievement_rate,
    st.currency
FROM sales_transactions st
JOIN customers c ON c.customer_id = st.customer_id
JOIN products p ON p.product_id = st.product_id
JOIN sales_reps sr ON sr.sales_rep_id = st.sales_rep_id
LEFT JOIN monthly_targets mt
    ON mt.month::date = DATE_TRUNC('month', st.order_date)::date
    AND mt.region = c.region
    AND mt.product_category = p.product_category
    AND mt.sales_rep_id = st.sales_rep_id;
