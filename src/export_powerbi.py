"""Build a flat Power BI-ready dashboard export."""

from __future__ import annotations

import pandas as pd

from config import POWERBI_DIR, PROCESSED_DIR, REPORTS_DIR, ensure_directories


def main() -> None:
    ensure_directories()
    sales = pd.read_csv(PROCESSED_DIR / "sales_enriched.csv")
    targets = pd.read_csv(PROCESSED_DIR / "monthly_targets.csv")
    customer_summary = pd.read_csv(REPORTS_DIR / "customer_sales_summary.csv")
    product_summary = pd.read_csv(REPORTS_DIR / "product_sales_summary.csv")

    target_keys = ["month", "region", "product_category", "sales_rep_id"]
    export = sales.merge(
        targets,
        left_on=["reporting_month", "region", "product_category", "sales_rep_id"],
        right_on=target_keys,
        how="left",
    )
    export = export.merge(
        customer_summary[["customer_id", "customer_value_band", "customer_status", "revenue_rank"]],
        on="customer_id",
        how="left",
    ).merge(
        product_summary[["product_id", "product_performance_band", "revenue_share"]],
        on="product_id",
        how="left",
    )

    export["target_achievement_rate"] = (export["net_revenue"] / export["revenue_target"]).where(export["revenue_target"].ne(0), 0).fillna(0)
    export["clean_order_month"] = export["reporting_month"]
    export["gross_margin_pct"] = (export["gross_margin"] / export["net_revenue"]).where(export["net_revenue"].ne(0), 0).fillna(0)

    columns = [
        "transaction_id",
        "clean_order_month",
        "order_date",
        "invoice_date",
        "customer_id",
        "customer_name",
        "country",
        "region",
        "industry",
        "customer_segment",
        "customer_value_band",
        "customer_status",
        "product_id",
        "product_name",
        "product_category",
        "product_family",
        "product_performance_band",
        "sales_rep_id",
        "sales_rep_name",
        "team",
        "manager",
        "channel",
        "dashboard_order_status",
        "quantity",
        "unit_price",
        "discount_rate",
        "discount_amount",
        "gross_revenue",
        "net_revenue",
        "cost",
        "gross_margin",
        "gross_margin_pct",
        "revenue_target",
        "margin_target",
        "volume_target",
        "target_achievement_rate",
        "currency",
    ]
    dashboard = export[columns].copy()
    dashboard.columns = [column.replace("_", " ") for column in dashboard.columns]
    dashboard.to_csv(POWERBI_DIR / "powerbi_sales_dashboard.csv", index=False)
    print(f"Created Power BI-ready dashboard export in {POWERBI_DIR}")


if __name__ == "__main__":
    main()
