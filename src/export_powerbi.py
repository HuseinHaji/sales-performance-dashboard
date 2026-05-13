import pandas as pd
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parents[1]
PROCESSED_PATH = BASE_PATH / 'data' / 'processed'
POWERBI_PATH = BASE_PATH / 'data' / 'powerbi'


def main():
    POWERBI_PATH.mkdir(parents=True, exist_ok=True)
    customers = pd.read_csv(PROCESSED_PATH / 'dim_customer.csv')
    products = pd.read_csv(PROCESSED_PATH / 'dim_product.csv')
    regions = pd.read_csv(PROCESSED_PATH / 'dim_region.csv')
    channels = pd.read_csv(PROCESSED_PATH / 'dim_channel.csv')
    date = pd.read_csv(PROCESSED_PATH / 'dim_date.csv')
    sales = pd.read_csv(PROCESSED_PATH / 'fact_sales.csv')
    targets = pd.read_csv(PROCESSED_PATH / 'fact_targets.csv')

    sales = sales.merge(customers, on='customer_id', how='left')
    sales = sales.merge(products, on='product_id', how='left')
    sales = sales.merge(regions, on='region_id', how='left')
    sales = sales.merge(channels, on='channel_id', how='left')
    sales = sales.merge(date, on='month_key', how='left')

    sales_dashboard = sales.copy()
    sales_dashboard.to_csv(POWERBI_PATH / 'sales_dashboard_dataset.csv', index=False)

    monthly_kpi = sales.groupby(['month_key', 'month_label'], as_index=False).agg(
        total_revenue=('revenue', 'sum'),
        total_profit=('profit', 'sum'),
        avg_margin=('margin', 'mean'),
        customer_count=('customer_id', 'nunique')
    ).sort_values('month_key')
    monthly_kpi.to_csv(POWERBI_PATH / 'monthly_kpi_summary.csv', index=False)

    product_perf = sales.groupby(['product_category'], as_index=False).agg(
        revenue=('revenue', 'sum'),
        profit=('profit', 'sum'),
        margin=('margin', 'mean')
    ).sort_values('revenue', ascending=False)
    product_perf.to_csv(POWERBI_PATH / 'product_performance.csv', index=False)

    region_perf = sales.groupby(['region_name'], as_index=False).agg(
        revenue=('revenue', 'sum'),
        profit=('profit', 'sum'),
        margin=('margin', 'mean')
    ).sort_values('revenue', ascending=False)
    region_perf.to_csv(POWERBI_PATH / 'region_performance.csv', index=False)

    customer_perf = sales.groupby(['customer_id', 'customer_name'], as_index=False).agg(
        revenue=('revenue', 'sum'),
        profit=('profit', 'sum'),
        average_order_value=('revenue', lambda x: x.sum() / max(len(x), 1))
    ).sort_values('revenue', ascending=False)
    customer_perf.to_csv(POWERBI_PATH / 'customer_performance.csv', index=False)

    print('Power BI sales outputs saved to', POWERBI_PATH)


if __name__ == '__main__':
    main()
