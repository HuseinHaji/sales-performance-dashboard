from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def test_monthly_kpi_ranges_are_valid():
    monthly = pd.read_csv(ROOT / "output/reports/monthly_sales_summary.csv")
    assert (monthly["net_revenue"] >= 0).all()
    assert monthly["gross_margin_pct"].between(-1, 1).all()
    assert (monthly["target_achievement_rate"] >= 0).all()
    assert monthly["year_to_date_revenue"].notna().all()


def test_customer_product_region_bands_exist():
    customers = pd.read_csv(ROOT / "output/reports/customer_sales_summary.csv")
    products = pd.read_csv(ROOT / "output/reports/product_sales_summary.csv")
    regions = pd.read_csv(ROOT / "output/reports/region_sales_summary.csv")
    assert customers["customer_value_band"].notna().all()
    assert products["product_performance_band"].notna().all()
    assert regions["region_performance_band"].notna().all()


def test_margin_calculation_is_consistent_in_dashboard_export():
    dashboard = pd.read_csv(ROOT / "output/powerbi/powerbi_sales_dashboard.csv")
    difference = (dashboard["gross margin"] - (dashboard["net revenue"] - dashboard["cost"])).abs()
    assert difference.max() <= 0.02
