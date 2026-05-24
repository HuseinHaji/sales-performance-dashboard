# Technical Notes: Sales Performance Dashboard

## Dataset Design

The project uses a synthetic B2B sales dataset with transaction, customer, product, sales rep, target, and calendar tables. The grain of `sales_transactions.csv` is one sales order line. The Power BI export keeps this transaction grain and enriches it with customer, product, sales rep, target, and segmentation fields.

## Pipeline Architecture

1. `src/generate_synthetic_data.py` creates deterministic raw CSV files.
2. `src/validate_data.py` checks schemas, keys, referential integrity, numeric ranges, dates, statuses, and margin calculations.
3. `src/transform_data.py` creates processed tables and an enriched sales model.
4. `src/calculate_kpis.py` builds monthly, customer, product, and region KPI outputs.
5. `src/sales_analysis.py` creates recruiter-readable business analysis outputs.
6. `src/export_powerbi.py` creates a flat BI-ready export.
7. `src/app.py` presents a Streamlit executive dashboard prototype.

## Validation Checks

The validation layer writes `output/audit/data_quality_report.csv` with check name, table, status, records checked, failed records, failure rate, severity, and timestamp. Checks include required columns, duplicate keys, foreign key consistency, non-negative revenue and cost, positive quantity, valid discounts, valid statuses, valid active flags, date consistency, and gross margin consistency.

## KPI Formulas

- `gross_margin = net_revenue - cost`
- `gross_margin_pct = gross_margin / net_revenue`
- `avg_order_value = net_revenue / total_orders`
- `target_achievement_rate = net_revenue / revenue_target`
- `month_over_month_growth = current_month_net_revenue / prior_month_net_revenue - 1`
- `year_to_date_revenue = cumulative net revenue by year`
- `revenue_share = product_revenue / total_revenue`
- `customer_concentration = top_10_customer_revenue / total_revenue`

## Sales Performance Logic

Customer bands:

- Strategic Accounts
- Growth Accounts
- Stable Accounts
- Low-Activity Accounts
- At-Risk / Declining Accounts

Product bands:

- Revenue Drivers
- Margin Leaders
- Volume Products
- Discount-Sensitive Products
- Underperforming Products

Region bands:

- Above Target
- On Track
- Below Target
- Needs Attention

## SQL Layer

The SQL folder shows PostgreSQL-style analytical queries for monthly overview, revenue and margin analysis, target achievement, customer performance, product performance, regional/channel analysis, a simple forecast base, and a dashboard export base table. These are written as portfolio-readable examples and assume equivalent table names in a PostgreSQL database.

## Power BI Export Design

`output/powerbi/powerbi_sales_dashboard.csv` is a flat transaction-level table with clean column names and dashboard-ready categories. It includes customer, product, sales rep, region, channel, order status, revenue, margin, discount, target, and segmentation fields.

## Testing Approach

The pytest suite runs the pipeline and verifies:

- raw files are generated
- report files are created
- required columns exist
- KPI values are in valid ranges
- margin calculations are consistent
- validation checks pass
- duplicate transaction, customer, and product IDs do not exist
- Power BI export is not empty

## Known Limitations

- The dataset is synthetic and not connected to a real CRM, ERP, or data warehouse.
- Forecasting is a simple baseline demonstration.
- SQL files are PostgreSQL-style examples and are not connected to a live database in this repo.
- Streamlit is a dashboard prototype, while Power BI report screenshots should be created manually from the exported CSV.

## Future Extensions

- Add dbt models or a PostgreSQL loader.
- Add year-over-year growth and cohort analysis.
- Add pipeline coverage, win rate, and sales cycle metrics.
- Add Power BI report screenshots and a published dashboard walkthrough.
- Add automated visual regression checks for the Streamlit dashboard.
