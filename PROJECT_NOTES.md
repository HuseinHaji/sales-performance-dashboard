# Project Notes — Sales Performance Dashboard

## Business problem
Provide a performance dashboard for a fictional sales organisation to track revenue, profit, margin, target achievement, and regional performance.

## What I built
- Synthetic sales data generation and transformation with `src/generate_sales_data.py` and `src/transform_sales_data.py`.
- KPI and dashboard-ready SQL views in `sql/`.
- Power BI-ready CSV outputs in `data/powerbi/`.
- Streamlit demo at `src/app.py` for quick validation and storytelling.

## Key technical points
- Built a data model with customers, products, regions, channels, and targets.
- Focused on business-critical KPIs: revenue growth, margin, target achievement, top customers.
- Added Docker and CI to ensure reproducible demos and smoke testing.
- Included sample data and unit tests to support maintainability.

## Project story
1. Challenge: decision-makers require accurate, timely visibility into sales performance.
2. Solution: design a modular ETL pipeline with analytics-ready outputs and a lightweight demo.
3. Impact: supports executive review and operational follow-up with actionable metrics.
4. Tradeoffs: kept the dataset synthetic but structured for realistic sales reporting.

## Lessons and improvements
- Next step: add time-series growth comparisons and pipeline forecasting.
- Key points: highlight KPIs, data validation, and how the dashboard aligns with strategic priorities.
