# Sales & Performance Dashboard

## Business Context

This project simulates a commercial performance dashboard for a fictional B2B sales organisation. The dashboard captures revenue, profit, margin, target achievement, regional performance, product metrics, and customer insights.

It supports sales managers and leaders in monthly performance review and strategic planning.

## Business Value

- Tracks revenue growth and margin performance.
- Highlights top customers, products, regions and channels.
- Compares actual sales against targets.
- Supports operational decision making and sales enablement.

## Tech Stack

- Python 3.10+ (pandas, numpy)
- PostgreSQL-style SQL
- Power BI-ready CSV files
- Jupyter Notebook for analysis

## Dataset

The data is synthetic and created to reflect a realistic commercial sales process. It includes customers, products, regions, channels, order lines, revenue, discounts, costs, profit, and targets.

## Data Model

- `dim_customer`: customer master data.
- `dim_product`: product reference table.
- `dim_region`: region master table.
- `dim_channel`: sales channel table.
- `dim_date`: monthly period table.
- `fact_sales`: sales order line data.
- `fact_targets`: monthly sales targets.
- Dashboard outputs in `data/powerbi/`.

## Key KPIs

- Total revenue
- Total profit
- Gross margin
- Revenue growth
- Monthly revenue trend
- Target achievement
- Sales by product category
- Sales by region
- Sales by channel
- Top customers and products
- Average order value
- Active customer count

## Project Structure

```text
sales-performance-dashboard/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/
│   ├── processed/
│   └── powerbi/
├── sql/
│   ├── 01_create_sales_schema.sql
│   ├── 02_sales_kpi_queries.sql
│   └── 03_dashboard_views.sql
├── src/
│   ├── generate_sales_data.py
│   ├── transform_sales_data.py
│   └── export_powerbi.py
├── notebooks/
│   └── sales_performance_analysis.ipynb
└── screenshots/
    └── .gitkeep
```

## How to Run

```bash
cd sales-performance-dashboard
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/generate_sales_data.py
python src/transform_sales_data.py
python src/export_powerbi.py
```

For Windows:

```powershell
.venv\Scriptsctivate
```

## Dashboard Design

Power BI pages:

1. Executive Sales Overview
2. Product Performance
3. Region & Channel Analysis
4. Customer Trends
5. Target vs Actual

## Example Insights

- Revenue growth is strongest in the West region and the Industrial product category.
- Target achievement is highest for channel E-commerce and lowest for direct sales in one month.
- Top customers contribute a significant share of profit, while mid-tier customers support margin stability.

## Future Improvements

- Add year-over-year comparisons.
- Integrate customer retention and pipeline metrics.
- Add scenario planning for target setting.

## Disclaimer

This project uses fully synthetic data created for portfolio demonstration purposes. It does not contain confidential, proprietary, or real company data.
