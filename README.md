# Sales Performance Dashboard

End-to-end sales analytics project that converts transaction data into executive KPIs, product and customer performance views, and commercial follow-up actions.

## Business Goal

Sales leaders need more than monthly revenue: they need margin visibility, customer concentration, product performance, and clear actions. This project prepares those layers from raw orders into dashboard-ready CSV tables.

## Architecture

```mermaid
flowchart LR
    A[Sales Orders CSV] --> B[Schema Validation]
    B --> C[KPI Aggregation Engine]
    C --> D[Monthly Trend KPIs]
    C --> E[Product Performance]
    C --> F[Customer Performance]
    D --> G[Executive Summary]
    E --> H[Pipeline Actions]
    F --> H
```

## Repository Structure

```text
.
├── data/
│   └── sales.csv
├── output/
│   ├── customer_performance.csv
│   ├── executive_summary.csv
│   ├── monthly_sales_kpis.csv
│   ├── pipeline_actions.csv
│   └── product_performance.csv
├── sql/
│   └── sales_kpis.sql
└── src/
    └── build_kpis.py
```

## What The Pipeline Does

- Validates the transaction schema before aggregation.
- Calculates revenue, cost, gross margin, margin percentage, and average order value.
- Produces monthly, product, and customer performance tables.
- Builds an executive summary for top-line dashboard tiles.
- Creates commercial action recommendations for low-margin products and high-value customers.
- Includes SQL examples for warehouse-style KPI generation.

## Outputs

| File | Purpose |
| --- | --- |
| `output/monthly_sales_kpis.csv` | Monthly trend metrics for revenue, orders, margin, and average order value. |
| `output/product_performance.csv` | Product-level revenue and margin performance. |
| `output/customer_performance.csv` | Customer-level revenue and margin performance. |
| `output/executive_summary.csv` | One-row dashboard summary for leadership. |
| `output/pipeline_actions.csv` | Follow-up actions based on margin and account concentration. |

## Run Locally

```bash
python3 src/build_kpis.py
```

No third-party packages are required; the project uses the Python standard library.

## Skills Demonstrated

Sales KPI modeling, commercial analytics, margin analysis, dashboard data modeling, CSV data engineering, and SQL-to-Python analytical parity.
