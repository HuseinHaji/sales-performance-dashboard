with kpis as (
  select
    month,
    product,
    customer,
    revenue_eur,
    cost_eur,
    revenue_eur - cost_eur as gross_margin_eur
  from sales
)
select
  month,
  count(*) as orders,
  sum(revenue_eur) as revenue_eur,
  sum(gross_margin_eur) as gross_margin_eur,
  sum(gross_margin_eur) / sum(revenue_eur) as gross_margin_pct,
  sum(revenue_eur) / count(*) as avg_order_value_eur,
  count(distinct customer) as active_customers,
  count(distinct product) as active_products
from kpis
group by month
order by month;
