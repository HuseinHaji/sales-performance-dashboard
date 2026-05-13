select
  month,
  count(*) as orders,
  sum(revenue_eur) as revenue_eur,
  sum(revenue_eur - cost_eur) as gross_margin_eur,
  sum(revenue_eur - cost_eur) / sum(revenue_eur) as gross_margin_pct
from sales
group by month
order by month;

