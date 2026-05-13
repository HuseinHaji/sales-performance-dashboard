from collections import defaultdict
from csv import DictReader, DictWriter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "sales.csv"
OUTPUT = ROOT / "output" / "monthly_sales_kpis.csv"


def main():
    with INPUT.open(newline="") as file:
        rows = list(DictReader(file))

    monthly = defaultdict(lambda: {"orders": 0, "revenue": 0.0, "cost": 0.0})
    for row in rows:
        bucket = monthly[row["month"]]
        bucket["orders"] += 1
        bucket["revenue"] += float(row["revenue_eur"])
        bucket["cost"] += float(row["cost_eur"])

    output = []
    for month, values in sorted(monthly.items()):
        margin = values["revenue"] - values["cost"]
        output.append(
            {
                "month": month,
                "orders": values["orders"],
                "revenue_eur": round(values["revenue"], 2),
                "gross_margin_eur": round(margin, 2),
                "gross_margin_pct": round(margin / values["revenue"], 3),
            }
        )

    OUTPUT.parent.mkdir(exist_ok=True)
    with OUTPUT.open("w", newline="") as file:
        writer = DictWriter(file, fieldnames=output[0].keys())
        writer.writeheader()
        writer.writerows(output)

    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()

