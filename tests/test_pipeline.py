import csv
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path):
    with path.open(newline="") as file:
        return list(csv.DictReader(file))


def test_pipeline_generates_sales_performance_outputs():
    result = subprocess.run(
        [sys.executable, "src/build_kpis.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "sales dashboard outputs" in result.stdout

    executive = read_csv(ROOT / "output" / "executive_summary.csv")
    forecast = read_csv(ROOT / "output" / "revenue_forecast.csv")
    bridge = read_csv(ROOT / "output" / "margin_bridge.csv")
    actions = read_csv(ROOT / "output" / "pipeline_actions.csv")

    assert len(executive) == 1
    assert float(executive[0]["revenue_eur"]) > 0
    assert forecast[0]["method"] == "three_month_revenue_average"
    assert len(bridge) == 3
    assert actions
