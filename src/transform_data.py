"""Create cleaned and enriched sales tables from the raw synthetic dataset."""

from __future__ import annotations

import pandas as pd

from config import PROCESSED_DIR, RAW_DIR, ensure_directories


def read_raw() -> dict[str, pd.DataFrame]:
    return {
        "customers": pd.read_csv(RAW_DIR / "customers.csv", parse_dates=["onboarding_date"]),
        "products": pd.read_csv(RAW_DIR / "products.csv"),
        "sales_reps": pd.read_csv(RAW_DIR / "sales_reps.csv", parse_dates=["hire_date"]),
        "calendar": pd.read_csv(RAW_DIR / "calendar.csv", parse_dates=["date"]),
        "sales_transactions": pd.read_csv(RAW_DIR / "sales_transactions.csv", parse_dates=["order_date", "invoice_date"]),
        "monthly_targets": pd.read_csv(RAW_DIR / "monthly_targets.csv"),
    }


def enrich_sales(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    sales = tables["sales_transactions"].copy()
    customers = tables["customers"]
    products = tables["products"]
    reps = tables["sales_reps"]

    enriched = (
        sales.merge(customers, on="customer_id", how="left")
        .merge(products, on="product_id", how="left", suffixes=("", "_product"))
        .merge(reps, on="sales_rep_id", how="left", suffixes=("", "_sales_rep"))
    )
    enriched["reporting_month"] = enriched["order_date"].dt.to_period("M").astype(str)
    enriched["year"] = enriched["order_date"].dt.year
    enriched["quarter"] = "Q" + enriched["order_date"].dt.quarter.astype(str)
    enriched["invoice_lag_days"] = (enriched["invoice_date"] - enriched["order_date"]).dt.days
    enriched["gross_margin_pct"] = (enriched["gross_margin"] / enriched["net_revenue"]).where(enriched["net_revenue"].ne(0), 0).round(4)
    enriched["discount_amount"] = (enriched["gross_revenue"] - enriched["net_revenue"]).round(2)
    enriched["is_closed_order"] = enriched["order_status"].isin(["Invoiced", "Shipped"])
    enriched["dashboard_order_status"] = enriched["order_status"].map(
        {"Invoiced": "Closed", "Shipped": "Closed", "Open": "Open", "Cancelled": "Cancelled"}
    )
    return enriched


def main() -> None:
    ensure_directories()
    tables = read_raw()
    for name, frame in tables.items():
        frame.to_csv(PROCESSED_DIR / f"{name}.csv", index=False)

    enriched = enrich_sales(tables)
    enriched.to_csv(PROCESSED_DIR / "sales_enriched.csv", index=False)
    print(f"Created processed sales tables in {PROCESSED_DIR}")


if __name__ == "__main__":
    main()
