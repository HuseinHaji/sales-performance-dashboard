"""Calculate management-ready sales KPI report tables."""

from __future__ import annotations

import numpy as np
import pandas as pd

from config import PROCESSED_DIR, REPORTS_DIR, ensure_directories


def safe_pct(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    return (numerator / denominator.replace(0, np.nan)).fillna(0)


def band_customer(row: pd.Series) -> str:
    if row["revenue_rank"] <= 10 and row["gross_margin_pct"] >= 0.40:
        return "Strategic Accounts"
    if row["total_revenue"] > row["total_revenue_median"] and row["order_count"] >= 8:
        return "Growth Accounts"
    if row["order_count"] >= 5:
        return "Stable Accounts"
    if row["customer_status"] == "At Risk":
        return "At-Risk / Declining Accounts"
    return "Low-Activity Accounts"


def band_product(row: pd.Series) -> str:
    if row["revenue_share"] >= 0.10:
        return "Revenue Drivers"
    if row["gross_margin_pct"] >= 0.52:
        return "Margin Leaders"
    if row["quantity_sold"] >= row["quantity_sold_median"]:
        return "Volume Products"
    if row["avg_discount_rate"] >= 0.12:
        return "Discount-Sensitive Products"
    return "Underperforming Products"


def band_region(target_rate: float) -> str:
    if target_rate >= 1.05:
        return "Above Target"
    if target_rate >= 0.95:
        return "On Track"
    if target_rate >= 0.85:
        return "Below Target"
    return "Needs Attention"


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    sales = pd.read_csv(PROCESSED_DIR / "sales_enriched.csv", parse_dates=["order_date", "invoice_date"])
    targets = pd.read_csv(PROCESSED_DIR / "monthly_targets.csv")
    closed_sales = sales[sales["is_closed_order"].eq(True)].copy()
    return closed_sales, targets


def monthly_summary(sales: pd.DataFrame, targets: pd.DataFrame) -> pd.DataFrame:
    monthly_targets = targets.groupby("month", as_index=False).agg(revenue_target=("revenue_target", "sum"))
    summary = (
        sales.groupby("reporting_month", as_index=False)
        .agg(
            total_revenue=("gross_revenue", "sum"),
            net_revenue=("net_revenue", "sum"),
            gross_margin=("gross_margin", "sum"),
            total_orders=("transaction_id", "nunique"),
            total_quantity=("quantity", "sum"),
            active_customers=("customer_id", "nunique"),
        )
        .merge(monthly_targets, left_on="reporting_month", right_on="month", how="left")
        .drop(columns=["month"])
        .sort_values("reporting_month")
    )
    summary["gross_margin_pct"] = safe_pct(summary["gross_margin"], summary["net_revenue"]).round(4)
    summary["avg_order_value"] = safe_pct(summary["net_revenue"], summary["total_orders"]).round(2)
    summary["target_achievement_rate"] = safe_pct(summary["net_revenue"], summary["revenue_target"]).round(4)
    summary["month_over_month_growth"] = summary["net_revenue"].pct_change().fillna(0).round(4)
    summary["year_to_date_revenue"] = summary.groupby(summary["reporting_month"].str[:4])["net_revenue"].cumsum().round(2)
    return summary[
        [
            "reporting_month",
            "total_revenue",
            "net_revenue",
            "gross_margin",
            "gross_margin_pct",
            "total_orders",
            "total_quantity",
            "active_customers",
            "avg_order_value",
            "revenue_target",
            "target_achievement_rate",
            "month_over_month_growth",
            "year_to_date_revenue",
        ]
    ].round(2)


def customer_summary(sales: pd.DataFrame) -> pd.DataFrame:
    summary = (
        sales.groupby(["customer_id", "customer_name", "country", "region", "industry", "customer_segment"], as_index=False)
        .agg(
            total_revenue=("net_revenue", "sum"),
            gross_margin=("gross_margin", "sum"),
            order_count=("transaction_id", "nunique"),
            last_order_date=("order_date", "max"),
        )
        .sort_values("total_revenue", ascending=False)
    )
    summary["gross_margin_pct"] = safe_pct(summary["gross_margin"], summary["total_revenue"]).round(4)
    summary["avg_order_value"] = safe_pct(summary["total_revenue"], summary["order_count"]).round(2)
    latest_order = pd.to_datetime(summary["last_order_date"]).max()
    days_since = (latest_order - pd.to_datetime(summary["last_order_date"])).dt.days
    summary["customer_status"] = np.where(days_since > 120, "At Risk", "Active")
    summary["revenue_rank"] = summary["total_revenue"].rank(method="dense", ascending=False).astype(int)
    summary["margin_rank"] = summary["gross_margin"].rank(method="dense", ascending=False).astype(int)
    summary["total_revenue_median"] = summary["total_revenue"].median()
    summary["customer_value_band"] = summary.apply(band_customer, axis=1)
    return summary.drop(columns=["total_revenue_median"]).round(2)


def product_summary(sales: pd.DataFrame) -> pd.DataFrame:
    total_revenue = sales["net_revenue"].sum()
    summary = (
        sales.groupby(["product_id", "product_name", "product_category", "product_family"], as_index=False)
        .agg(
            total_revenue=("net_revenue", "sum"),
            gross_margin=("gross_margin", "sum"),
            quantity_sold=("quantity", "sum"),
            order_count=("transaction_id", "nunique"),
            avg_discount_rate=("discount_rate", "mean"),
        )
        .sort_values("total_revenue", ascending=False)
    )
    summary["gross_margin_pct"] = safe_pct(summary["gross_margin"], summary["total_revenue"]).round(4)
    summary["revenue_share"] = (summary["total_revenue"] / total_revenue).round(4)
    summary["quantity_sold_median"] = summary["quantity_sold"].median()
    summary["product_performance_band"] = summary.apply(band_product, axis=1)
    return summary.drop(columns=["quantity_sold_median"]).round(2)


def region_summary(sales: pd.DataFrame, targets: pd.DataFrame) -> pd.DataFrame:
    target_by_region = targets.groupby("region", as_index=False).agg(revenue_target=("revenue_target", "sum"))
    top_categories = (
        sales.groupby(["region", "product_category"], as_index=False)
        .agg(category_revenue=("net_revenue", "sum"))
        .sort_values(["region", "category_revenue"], ascending=[True, False])
        .drop_duplicates("region")
        .rename(columns={"product_category": "top_product_category"})
    )
    summary = (
        sales.groupby(["region", "country"], as_index=False)
        .agg(
            total_revenue=("net_revenue", "sum"),
            gross_margin=("gross_margin", "sum"),
            order_count=("transaction_id", "nunique"),
            active_customers=("customer_id", "nunique"),
        )
        .merge(target_by_region, on="region", how="left")
        .merge(top_categories[["region", "top_product_category"]], on="region", how="left")
    )
    summary["gross_margin_pct"] = safe_pct(summary["gross_margin"], summary["total_revenue"]).round(4)
    summary["target_achievement_rate"] = safe_pct(summary["total_revenue"], summary["revenue_target"]).round(4)
    summary["region_performance_band"] = summary["target_achievement_rate"].apply(band_region)
    return summary.round(2)


def main() -> None:
    ensure_directories()
    sales, targets = load_data()
    monthly = monthly_summary(sales, targets)
    customers = customer_summary(sales)
    products = product_summary(sales)
    regions = region_summary(sales, targets)

    monthly.to_csv(REPORTS_DIR / "monthly_sales_summary.csv", index=False)
    customers.to_csv(REPORTS_DIR / "customer_sales_summary.csv", index=False)
    products.to_csv(REPORTS_DIR / "product_sales_summary.csv", index=False)
    regions.to_csv(REPORTS_DIR / "region_sales_summary.csv", index=False)
    print(f"Created KPI report tables in {REPORTS_DIR}")


if __name__ == "__main__":
    main()
