import numpy as np
import pandas as pd
from pathlib import Path

RAW_PATH = Path(__file__).resolve().parents[1] / 'data' / 'raw'
RANDOM_SEED = 5050

REGIONS = ['North', 'South', 'East', 'West']
CHANNELS = ['Direct', 'Distributor', 'E-commerce', 'Partner']
PRODUCT_CATEGORIES = ['Industrial', 'Software', 'Hardware', 'Services']
PRODUCTS = [
    {'product_id': f'PRD{i:03d}', 'product_name': name, 'product_category': category}
    for i, (name, category) in enumerate([
        ('Industrial Pump', 'Industrial'),
        ('Analytics Suite', 'Software'),
        ('Control Panel', 'Hardware'),
        ('Service Contract', 'Services'),
        ('Energy Module', 'Industrial'),
        ('Cloud License', 'Software'),
        ('Hardware Kit', 'Hardware'),
        ('Maintenance Plan', 'Services'),
    ], start=1)
]
def generate_customers(rng):
    return pd.DataFrame([
        {
            'customer_id': f'CUST{i:03d}',
            'customer_name': f'Partner {i:02d}',
            'region': rng.choice(REGIONS),
            'customer_segment': rng.choice(['Strategic', 'Growth', 'Standard']),
        }
        for i in range(1, 61)
    ])


def generate_date_table():
    months = pd.date_range('2023-01-01', periods=24, freq='MS')
    return pd.DataFrame({
        'month_key': months.strftime('%Y-%m'),
        'month_start': months,
        'month_label': months.strftime('%b %Y'),
    })


def main():
    RAW_PATH.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(RANDOM_SEED)
    products = pd.DataFrame(PRODUCTS)
    customers = generate_customers(rng)
    regions = pd.DataFrame({'region_id': range(1, len(REGIONS)+1), 'region_name': REGIONS})
    channels = pd.DataFrame({'channel_id': range(1, len(CHANNELS)+1), 'channel_name': CHANNELS})

    date = generate_date_table()
    sales = []
    for idx, month in date.iterrows():
        period = pd.to_datetime(month['month_start'])
        for order_id in range(40):
            customer = customers.sample(n=1, random_state=rng.integers(1_000_000)).iloc[0]
            product = products.sample(n=1, random_state=rng.integers(1_000_000)).iloc[0]
            channel = channels.sample(n=1, random_state=rng.integers(1_000_000)).iloc[0]
            quantity = int(rng.integers(1, 12))
            unit_price = round(float(rng.uniform(1200, 25000)), 2)
            discount_rate = round(float(rng.uniform(0.0, 0.18)), 2)
            revenue = round(quantity * unit_price * (1 - discount_rate), 2)
            cost = round(quantity * unit_price * rng.uniform(0.55, 0.78), 2)
            profit = round(revenue - cost, 2)
            margin = round(profit / revenue if revenue else 0.0, 4)
            sales.append({
                'sales_id': f'SALE{idx+1:02d}{order_id+1:04d}',
                'customer_id': customer['customer_id'],
                'product_id': product['product_id'],
                'region_id': int(regions[regions.region_name == customer['region']]['region_id'].iloc[0]),
                'channel_id': int(channel['channel_id']),
                'month_key': month['month_key'],
                'order_date': period.date(),
                'quantity': quantity,
                'unit_price': unit_price,
                'discount_rate': discount_rate,
                'revenue': revenue,
                'cost': cost,
                'profit': profit,
                'margin': margin,
            })

    targets = []
    for _, month in date.iterrows():
        for _, region in regions.iterrows():
            target = round(rng.uniform(2_000_000, 4_500_000), 2)
            targets.append({'month_key': month['month_key'], 'region_id': region['region_id'], 'sales_target': target})

    customers.to_csv(RAW_PATH / 'dim_customer.csv', index=False)
    products.to_csv(RAW_PATH / 'dim_product.csv', index=False)
    regions.to_csv(RAW_PATH / 'dim_region.csv', index=False)
    channels.to_csv(RAW_PATH / 'dim_channel.csv', index=False)
    date.to_csv(RAW_PATH / 'dim_date.csv', index=False)
    pd.DataFrame(sales).to_csv(RAW_PATH / 'fact_sales.csv', index=False)
    pd.DataFrame(targets).to_csv(RAW_PATH / 'fact_targets.csv', index=False)
    print('Sales raw data generated to', RAW_PATH)

if __name__ == '__main__':
    main()
