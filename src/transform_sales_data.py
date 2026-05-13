import pandas as pd
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parents[1]
RAW_PATH = BASE_PATH / 'data' / 'raw'
PROCESSED_PATH = BASE_PATH / 'data' / 'processed'


def main():
    PROCESSED_PATH.mkdir(parents=True, exist_ok=True)
    dim_customer = pd.read_csv(RAW_PATH / 'dim_customer.csv')
    dim_product = pd.read_csv(RAW_PATH / 'dim_product.csv')
    dim_region = pd.read_csv(RAW_PATH / 'dim_region.csv')
    dim_channel = pd.read_csv(RAW_PATH / 'dim_channel.csv')
    dim_date = pd.read_csv(RAW_PATH / 'dim_date.csv')
    fact_sales = pd.read_csv(RAW_PATH / 'fact_sales.csv')
    fact_targets = pd.read_csv(RAW_PATH / 'fact_targets.csv')

    dim_customer.to_csv(PROCESSED_PATH / 'dim_customer.csv', index=False)
    dim_product.to_csv(PROCESSED_PATH / 'dim_product.csv', index=False)
    dim_region.to_csv(PROCESSED_PATH / 'dim_region.csv', index=False)
    dim_channel.to_csv(PROCESSED_PATH / 'dim_channel.csv', index=False)
    dim_date.to_csv(PROCESSED_PATH / 'dim_date.csv', index=False)
    fact_sales.to_csv(PROCESSED_PATH / 'fact_sales.csv', index=False)
    fact_targets.to_csv(PROCESSED_PATH / 'fact_targets.csv', index=False)
    print('Processed sales data saved to', PROCESSED_PATH)

if __name__ == '__main__':
    main()
