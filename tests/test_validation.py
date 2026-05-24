from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def test_validation_report_has_no_failed_checks():
    report = pd.read_csv(ROOT / "output/audit/data_quality_report.csv")
    assert not report.empty
    assert set(report["status"]) == {"pass"}


def test_raw_keys_are_unique():
    sales = pd.read_csv(ROOT / "data/raw/sales_transactions.csv")
    customers = pd.read_csv(ROOT / "data/raw/customers.csv")
    products = pd.read_csv(ROOT / "data/raw/products.csv")
    assert not sales["transaction_id"].duplicated().any()
    assert not customers["customer_id"].duplicated().any()
    assert not products["product_id"].duplicated().any()


def test_raw_numeric_values_are_valid():
    sales = pd.read_csv(ROOT / "data/raw/sales_transactions.csv")
    assert (sales[["gross_revenue", "net_revenue", "cost"]] >= 0).all().all()
    assert sales["discount_rate"].between(0, 1).all()
    assert (sales["quantity"] > 0).all()
