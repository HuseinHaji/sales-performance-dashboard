from collections import defaultdict
from csv import DictReader, DictWriter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "sales.csv"
OUTPUT_DIR = ROOT / "output"
REQUIRED_FIELDS = ["order_id", "month", "customer", "product", "revenue_eur", "cost_eur"]


def as_float(row, field):
    try:
        return float(row[field])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"{row.get('order_id', 'unknown')}: invalid {field}") from exc


def aggregate(rows, key):
    grouped = defaultdict(lambda: {"orders": 0, "revenue": 0.0, "cost": 0.0})
    for row in rows:
        bucket = grouped[row[key]]
        bucket["orders"] += 1
        bucket["revenue"] += as_float(row, "revenue_eur")
        bucket["cost"] += as_float(row, "cost_eur")

    output = []
    for segment, values in sorted(grouped.items()):
        margin = values["revenue"] - values["cost"]
        output.append(
            {
                key: segment,
                "orders": values["orders"],
                "revenue_eur": round(values["revenue"], 2),
                "gross_margin_eur": round(margin, 2),
                "gross_margin_pct": round(margin / values["revenue"], 3),
                "avg_order_value_eur": round(values["revenue"] / values["orders"], 2),
            }
        )
    return output


def build_exec_summary(rows, monthly):
    revenue = sum(as_float(row, "revenue_eur") for row in rows)
    cost = sum(as_float(row, "cost_eur") for row in rows)
    margin = revenue - cost
    best_month = max(monthly, key=lambda row: row["revenue_eur"])
    return [
        {
            "orders": len(rows),
            "revenue_eur": round(revenue, 2),
            "gross_margin_eur": round(margin, 2),
            "gross_margin_pct": round(margin / revenue, 3),
            "avg_order_value_eur": round(revenue / len(rows), 2),
            "best_month": best_month["month"],
            "best_month_revenue_eur": best_month["revenue_eur"],
        }
    ]


def build_pipeline_actions(product_rows, customer_rows):
    actions = []
    for row in product_rows:
        if row["gross_margin_pct"] < 0.48:
            actions.append(
                {
                    "focus_area": "product",
                    "segment": row["product"],
                    "metric": "gross_margin_pct",
                    "value": row["gross_margin_pct"],
                    "recommended_action": "Review pricing and delivery cost",
                }
            )
    for row in customer_rows:
        if row["revenue_eur"] >= 25000:
            actions.append(
                {
                    "focus_area": "customer",
                    "segment": row["customer"],
                    "metric": "revenue_eur",
                    "value": row["revenue_eur"],
                    "recommended_action": "Protect account and propose expansion",
                }
            )
    return actions


def build_forecast(monthly):
    latest = monthly[-1]
    avg_revenue = sum(row["revenue_eur"] for row in monthly) / len(monthly)
    avg_margin_pct = sum(row["gross_margin_pct"] for row in monthly) / len(monthly)
    next_month = "2026-04"
    return [
        {
            "forecast_month": next_month,
            "method": "three_month_revenue_average",
            "forecast_revenue_eur": round(avg_revenue, 2),
            "forecast_gross_margin_eur": round(avg_revenue * avg_margin_pct, 2),
            "forecast_gross_margin_pct": round(avg_margin_pct, 3),
            "latest_month": latest["month"],
            "latest_month_revenue_eur": latest["revenue_eur"],
        }
    ]


def build_margin_bridge(monthly):
    rows = []
    previous = None
    for row in monthly:
        if previous is None:
            rows.append(
                {
                    "month": row["month"],
                    "revenue_change_eur": 0,
                    "margin_change_eur": 0,
                    "margin_pct_change": 0,
                }
            )
        else:
            rows.append(
                {
                    "month": row["month"],
                    "revenue_change_eur": round(row["revenue_eur"] - previous["revenue_eur"], 2),
                    "margin_change_eur": round(row["gross_margin_eur"] - previous["gross_margin_eur"], 2),
                    "margin_pct_change": round(row["gross_margin_pct"] - previous["gross_margin_pct"], 3),
                }
            )
        previous = row
    return rows


def write_csv(path, rows):
    if not rows:
        return
    with path.open("w", newline="") as file:
        writer = DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def main():
    with INPUT.open(newline="") as file:
        rows = list(DictReader(file))
    missing = [field for field in REQUIRED_FIELDS if rows and field not in rows[0]]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")

    monthly = aggregate(rows, "month")
    products = sorted(aggregate(rows, "product"), key=lambda row: row["revenue_eur"], reverse=True)
    customers = sorted(aggregate(rows, "customer"), key=lambda row: row["revenue_eur"], reverse=True)

    OUTPUT_DIR.mkdir(exist_ok=True)
    write_csv(OUTPUT_DIR / "monthly_sales_kpis.csv", monthly)
    write_csv(OUTPUT_DIR / "product_performance.csv", products)
    write_csv(OUTPUT_DIR / "customer_performance.csv", customers)
    write_csv(OUTPUT_DIR / "executive_summary.csv", build_exec_summary(rows, monthly))
    write_csv(OUTPUT_DIR / "pipeline_actions.csv", build_pipeline_actions(products, customers))
    write_csv(OUTPUT_DIR / "revenue_forecast.csv", build_forecast(monthly))
    write_csv(OUTPUT_DIR / "margin_bridge.csv", build_margin_bridge(monthly))

    print(f"Wrote sales dashboard outputs to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
