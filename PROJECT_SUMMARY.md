# Project Summary: Sales Performance Dashboard

## Problem

This simulated business case asks how sales teams can monitor revenue, margin, target achievement, and customer/product performance using a clean, automated, dashboard-ready analytics workflow.

## Solution

Built a synthetic sales performance analytics workflow that transforms transaction, customer, product, sales rep, and target data into validated KPI tables, business performance summaries, and a flat Power BI-ready export. The project also includes PostgreSQL-style analytics queries, pytest checks, Docker support, GitHub Actions, and a Streamlit executive dashboard demo.

## Workflow

```text
Synthetic raw files
-> data validation and audit report
-> enriched transaction model
-> monthly, customer, product, and region KPI tables
-> business analysis outputs
-> Power BI-ready export
-> Streamlit dashboard prototype
```

## Business Value

- Tracks revenue, margin, growth, order volume, active customers, and target achievement.
- Identifies top-performing customers, products, regions, channels, and sales reps.
- Segments customers, products, and regions into business-readable performance bands.
- Produces clean BI-ready datasets for dashboarding and management reporting.
- Adds validation checks to improve confidence in reporting outputs.

## Technical Skills Demonstrated

| Skill | Where demonstrated |
|---|---|
| Python | modular pipeline scripts in `src/` |
| pandas | joins, feature engineering, KPI tables, aggregations |
| numpy | deterministic synthetic data generation |
| SQL | CTEs, joins, windows, rankings, target analysis |
| Sales analytics | revenue, margin, product, customer, region, and rep performance |
| KPI design | margin %, MoM growth, YTD revenue, target achievement |
| Data validation | schema checks, referential integrity, audit report |
| Power BI-ready modeling | flat enriched export at transaction grain |
| Streamlit | interactive executive sales dashboard demo |
| Docker | containerized Streamlit workflow |
| CI/CD | GitHub Actions pipeline checks |
| pytest | output, schema, validation, and KPI tests |

## Outputs

- `output/reports/monthly_sales_summary.csv`
- `output/reports/customer_sales_summary.csv`
- `output/reports/product_sales_summary.csv`
- `output/reports/region_sales_summary.csv`
- `output/powerbi/powerbi_sales_dashboard.csv`
- `output/audit/data_quality_report.csv`

## How This Maps To Real Analyst Work

The project mirrors common BI and data analyst tasks: define KPIs, validate source data, prepare a clean reporting model, write SQL for business questions, produce dashboard-ready exports, document assumptions, and communicate commercial performance in management-friendly language.

All data is synthetic and the project is designed for portfolio demonstration.
