# Sales Performance Dashboard

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL--style-informational)
![pandas](https://img.shields.io/badge/pandas-analytics-green)
![Streamlit](https://img.shields.io/badge/Streamlit-demo-red)
![Tests](https://img.shields.io/badge/pytest-validation-brightgreen)
![Data](https://img.shields.io/badge/data-synthetic-lightgrey)

Sales Performance Dashboard is a synthetic business intelligence project that demonstrates how sales transactions, targets, products, customers, and regions can be transformed into KPI summaries, performance analysis, and dashboard-ready outputs.

## Business Context

A simulated B2B company wants to monitor commercial performance across customers, products, regions, sales channels, and months. Management needs a reliable view of revenue, gross margin, target achievement, growth, customer concentration, product contribution, and sales rep performance.

This portfolio implementation is designed to demonstrate a clean sales analytics workflow from raw synthetic data to BI-ready reporting tables and an executive Streamlit demo.

## Business Problem

Sales leaders often need to answer:

- Are revenue and margin growing month over month?
- Which regions, customers, products, and channels drive performance?
- Are teams achieving revenue, margin, and volume targets?
- Where are discounts affecting margin?
- Which outputs are ready for Power BI or management reporting?

## Solution Overview

The project builds a reproducible analytics workflow:

```text
Synthetic sales data
  -> data validation
  -> feature engineering
  -> KPI calculation
  -> margin, customer, product, and region analysis
  -> Power BI-ready export
  -> Streamlit executive dashboard
  -> portfolio-ready documentation
```

## Dataset Description

The dataset is fully synthetic and models a realistic B2B commercial analytics case.

- `customers.csv`: customer master data with country, region, industry, size, segment, onboarding date, and active flag.
- `products.csv`: product reference data with category, family, unit cost, list price, and active flag.
- `sales_transactions.csv`: transaction-level order data with quantity, pricing, discount, revenue, cost, margin, currency, and order status.
- `sales_reps.csv`: sales rep, team, region, manager, and hire date reference data.
- `monthly_targets.csv`: simulated revenue, margin, and volume targets by month, region, product category, and sales rep.
- `calendar.csv`: date, month, quarter, year, and month name reference table.

## Validation Layer

`src/validate_data.py` creates `output/audit/data_quality_report.csv` with checks for:

- required columns
- duplicate transaction, customer, and product IDs
- customer, product, and sales rep referential integrity
- non-negative revenue, unit price, and cost
- positive quantity
- discount rates between 0 and 1
- gross margin consistency
- order date before or equal to invoice date
- valid active flags and order statuses
- nulls in critical fields

## KPI Logic

The reporting layer calculates:

- total revenue and net revenue
- gross margin and gross margin percentage
- order count, quantity, active customers, and average order value
- month-over-month growth and year-to-date revenue
- target achievement rate
- revenue by product category, region, channel, and sales rep
- top customers and products
- discount impact
- revenue contribution share
- customer, product, and region performance bands
- simple forecast base in SQL using a three-month moving average

## SQL Analytics Layer

The `sql/` folder contains PostgreSQL-style reporting queries using CTEs, joins, aggregations, `CASE WHEN`, window functions, date logic, ranking, and dashboard export logic:

- `01_sales_overview.sql`
- `02_revenue_margin_analysis.sql`
- `03_target_achievement.sql`
- `04_customer_performance.sql`
- `05_product_performance.sql`
- `06_region_channel_analysis.sql`
- `07_sales_forecast_base.sql`
- `08_dashboard_export.sql`

## Dashboard Design

The Streamlit demo in `src/app.py` is structured like an executive sales dashboard:

- Page 1: Executive Overview with revenue, margin, orders, active customers, target achievement, trend, and growth.
- Page 2: Revenue & Margin with monthly revenue, channel revenue, category margin, and discount impact.
- Page 3: Product Performance with category revenue, top products, quantity sold, and product performance bands.
- Page 4: Customer Performance with top customers, value bands, concentration, average order value, and segment performance.
- Page 5: Region & Channel Analysis with region revenue, country view, channel performance, target achievement, and sales rep ranking.
- Page 6: Target Achievement with revenue vs target, margin vs target, volume target, and progress indicators.
- Page 7: Data Quality / Methodology with validation results and workflow notes.

## Repository Structure

```text
sales-performance-dashboard/
├── .github/workflows/
├── data/
│   ├── raw/
│   ├── processed/
│   └── reference/
├── output/
│   ├── reports/
│   ├── powerbi/
│   └── audit/
├── screenshots/
├── sql/
├── src/
│   ├── config.py
│   ├── generate_synthetic_data.py
│   ├── validate_data.py
│   ├── transform_data.py
│   ├── calculate_kpis.py
│   ├── sales_analysis.py
│   ├── export_powerbi.py
│   └── app.py
└── tests/
```

## How To Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

python src/generate_synthetic_data.py
python src/validate_data.py
python src/transform_data.py
python src/calculate_kpis.py
python src/sales_analysis.py
python src/export_powerbi.py
pytest
streamlit run src/app.py
```

## Outputs

- `output/reports/monthly_sales_summary.csv`
- `output/reports/customer_sales_summary.csv`
- `output/reports/product_sales_summary.csv`
- `output/reports/region_sales_summary.csv`
- `output/reports/executive_sales_insights.csv`
- `output/reports/top_10_customers.csv`
- `output/reports/top_10_products_by_margin.csv`
- `output/reports/region_performance_actions.csv`
- `output/powerbi/powerbi_sales_dashboard.csv`
- `output/audit/data_quality_report.csv`

## Example Insights

These are example analytical outputs from the synthetic sales dataset, not real business impact claims:

- Revenue and margin can be monitored by month with target achievement and year-to-date tracking.
- Customer value bands separate strategic, growth, stable, low-activity, and at-risk accounts.
- Product performance bands identify revenue drivers, margin leaders, volume products, discount-sensitive products, and underperforming products.
- The BI-ready export supports Power BI modeling at transaction grain with enriched customer, product, sales rep, target, and margin fields.

## Skills Demonstrated

| Skill | Where demonstrated |
|---|---|
| Python | pipeline scripts, synthetic data generation, transformations |
| pandas | joins, cleaning, KPI tables, aggregations |
| numpy | deterministic synthetic data generation |
| SQL | sales analysis queries, KPI logic, ranking queries |
| Sales analytics | revenue, margin, target, product, customer analysis |
| KPI design | revenue, margin, growth, target achievement metrics |
| Data validation | schema checks, audit report, duplicate checks |
| Power BI-ready modeling | flat dashboard export table |
| Streamlit | interactive executive sales dashboard |
| Docker | reproducible local deployment |
| CI/CD | automated tests through GitHub Actions |
| pytest | validation tests and output checks |
| Business analytics | commercial performance monitoring and dashboard storytelling |

## Limitations

- The data is synthetic and does not represent a real company.
- Forecasting is intentionally simple and used as a baseline demonstration.
- The Streamlit dashboard is a prototype for portfolio review, not a production BI application.
- Power BI screenshots should be added manually after building the report from the export.

## Future Improvements

- Add year-over-year comparisons after extending the synthetic date range.
- Add pipeline and opportunity data for sales funnel analytics.
- Add dbt models or PostgreSQL loading scripts.
- Add richer forecast methods and scenario planning.
- Add Power BI report screenshots and a short dashboard walkthrough.

## GitHub Repo Polish

Suggested GitHub About:

> Synthetic sales performance dashboard project using Python, SQL, Streamlit, validation checks, KPI logic, and Power BI-ready outputs.

Suggested Topics:

`sales-analytics`, `sales-dashboard`, `data-analytics`, `business-intelligence`, `python`, `sql`, `pandas`, `streamlit`, `powerbi`, `kpi-dashboard`, `portfolio-project`, `synthetic-data`

## Disclaimer

This project uses a synthetic sales dataset for a simulated business case. It is a portfolio implementation designed to demonstrate analytics engineering, sales analytics, KPI design, validation, and BI-ready output creation. It does not use or claim real company data or real business impact.
