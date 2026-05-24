import subprocess
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def run_pipeline() -> None:
    scripts = [
        "src/generate_synthetic_data.py",
        "src/validate_data.py",
        "src/transform_data.py",
        "src/calculate_kpis.py",
        "src/sales_analysis.py",
        "src/export_powerbi.py",
    ]
    for script in scripts:
        subprocess.run([sys.executable, script], cwd=ROOT, check=True, capture_output=True, text=True)


def test_pipeline_creates_expected_outputs():
    run_pipeline()
    expected_files = [
        "data/raw/sales_transactions.csv",
        "data/raw/customers.csv",
        "data/raw/products.csv",
        "output/reports/monthly_sales_summary.csv",
        "output/reports/customer_sales_summary.csv",
        "output/reports/product_sales_summary.csv",
        "output/reports/region_sales_summary.csv",
        "output/powerbi/powerbi_sales_dashboard.csv",
        "output/audit/data_quality_report.csv",
    ]
    for relative_path in expected_files:
        assert (ROOT / relative_path).exists(), relative_path


def test_powerbi_export_is_not_empty():
    run_pipeline()
    dashboard = pd.read_csv(ROOT / "output/powerbi/powerbi_sales_dashboard.csv")
    assert not dashboard.empty
    assert {"transaction id", "net revenue", "gross margin", "target achievement rate"}.issubset(dashboard.columns)
