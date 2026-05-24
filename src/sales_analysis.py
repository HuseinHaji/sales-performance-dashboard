"""Create additional business-readable sales analysis outputs."""

from __future__ import annotations

import pandas as pd

from config import REPORTS_DIR, ensure_directories


def main() -> None:
    ensure_directories()
    monthly = pd.read_csv(REPORTS_DIR / "monthly_sales_summary.csv")
    customers = pd.read_csv(REPORTS_DIR / "customer_sales_summary.csv")
    products = pd.read_csv(REPORTS_DIR / "product_sales_summary.csv")
    regions = pd.read_csv(REPORTS_DIR / "region_sales_summary.csv")

    executive_summary = pd.DataFrame(
        [
            {
                "analysis_area": "Executive Overview",
                "metric": "latest_month_revenue",
                "value": monthly.iloc[-1]["net_revenue"],
                "business_interpretation": "Most recent closed-order revenue in the synthetic sales dataset.",
            },
            {
                "analysis_area": "Margin",
                "metric": "average_gross_margin_pct",
                "value": round(monthly["gross_margin_pct"].mean(), 4),
                "business_interpretation": "Portfolio implementation margin indicator for commercial review.",
            },
            {
                "analysis_area": "Customer Concentration",
                "metric": "top_10_customer_revenue_share",
                "value": round(customers.head(10)["total_revenue"].sum() / customers["total_revenue"].sum(), 4),
                "business_interpretation": "Share of revenue contributed by the top ten synthetic customers.",
            },
            {
                "analysis_area": "Target Achievement",
                "metric": "average_target_achievement_rate",
                "value": round(monthly["target_achievement_rate"].mean(), 4),
                "business_interpretation": "Average revenue attainment against simulated monthly targets.",
            },
        ]
    )

    top_customers = customers.head(10).copy()
    top_products_by_margin = products.sort_values("gross_margin", ascending=False).head(10).copy()
    region_actions = regions[["region", "country", "target_achievement_rate", "region_performance_band"]].copy()

    executive_summary.to_csv(REPORTS_DIR / "executive_sales_insights.csv", index=False)
    top_customers.to_csv(REPORTS_DIR / "top_10_customers.csv", index=False)
    top_products_by_margin.to_csv(REPORTS_DIR / "top_10_products_by_margin.csv", index=False)
    region_actions.to_csv(REPORTS_DIR / "region_performance_actions.csv", index=False)
    print(f"Created business analysis outputs in {REPORTS_DIR}")


if __name__ == "__main__":
    main()
