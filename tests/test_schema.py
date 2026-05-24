from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def test_report_schemas_match_expected_columns():
    expected = {
        "output/reports/monthly_sales_summary.csv": {
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
        },
        "output/reports/customer_sales_summary.csv": {
            "customer_id",
            "customer_name",
            "country",
            "region",
            "industry",
            "customer_segment",
            "total_revenue",
            "gross_margin",
            "gross_margin_pct",
            "order_count",
            "avg_order_value",
            "last_order_date",
            "customer_value_band",
            "customer_status",
            "revenue_rank",
            "margin_rank",
        },
        "output/reports/product_sales_summary.csv": {
            "product_id",
            "product_name",
            "product_category",
            "product_family",
            "total_revenue",
            "gross_margin",
            "gross_margin_pct",
            "quantity_sold",
            "order_count",
            "avg_discount_rate",
            "revenue_share",
            "product_performance_band",
        },
        "output/reports/region_sales_summary.csv": {
            "region",
            "country",
            "total_revenue",
            "gross_margin",
            "gross_margin_pct",
            "order_count",
            "active_customers",
            "revenue_target",
            "target_achievement_rate",
            "top_product_category",
            "region_performance_band",
        },
    }
    for relative_path, columns in expected.items():
        frame = pd.read_csv(ROOT / relative_path)
        assert columns.issubset(frame.columns), relative_path
