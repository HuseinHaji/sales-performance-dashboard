"""Run schema and data quality checks for the synthetic sales dataset."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import numpy as np
import pandas as pd

from config import AUDIT_DIR, RAW_DIR, VALID_ACTIVE_FLAGS, VALID_ORDER_STATUSES, ensure_directories


REQUIRED_COLUMNS = {
    "customers": [
        "customer_id",
        "customer_name",
        "country",
        "region",
        "industry",
        "company_size",
        "customer_segment",
        "onboarding_date",
        "active_flag",
    ],
    "products": ["product_id", "product_name", "product_category", "product_family", "unit_cost", "list_price", "active_flag"],
    "sales_transactions": [
        "transaction_id",
        "customer_id",
        "product_id",
        "sales_rep_id",
        "channel",
        "order_date",
        "invoice_date",
        "quantity",
        "unit_price",
        "discount_rate",
        "gross_revenue",
        "net_revenue",
        "cost",
        "gross_margin",
        "currency",
        "order_status",
    ],
    "sales_reps": ["sales_rep_id", "sales_rep_name", "team", "region", "manager", "hire_date"],
    "monthly_targets": ["month", "region", "product_category", "sales_rep_id", "revenue_target", "margin_target", "volume_target"],
    "calendar": ["date", "month", "quarter", "year", "month_name"],
}


@dataclass
class CheckResult:
    check_name: str
    table_name: str
    status: str
    records_checked: int
    failed_records: int
    failure_rate: float
    severity: str
    check_timestamp: str


def load_raw_tables() -> dict[str, pd.DataFrame]:
    return {name: pd.read_csv(RAW_DIR / f"{name}.csv") for name in REQUIRED_COLUMNS}


def result(check_name: str, table_name: str, records_checked: int, failed_records: int, severity: str = "high") -> CheckResult:
    status = "pass" if failed_records == 0 else "fail"
    failure_rate = round(failed_records / records_checked, 4) if records_checked else 0.0
    return CheckResult(check_name, table_name, status, int(records_checked), int(failed_records), failure_rate, severity, datetime.utcnow().isoformat())


def validate_tables(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    checks: list[CheckResult] = []
    for table_name, required in REQUIRED_COLUMNS.items():
        frame = tables[table_name]
        missing = [column for column in required if column not in frame.columns]
        checks.append(result("required_columns_exist", table_name, len(required), len(missing), "critical"))
        if not missing:
            critical_nulls = int(frame[required].isna().sum().sum())
            checks.append(result("no_nulls_in_required_columns", table_name, len(frame) * len(required), critical_nulls, "high"))

    sales = tables["sales_transactions"]
    customers = tables["customers"]
    products = tables["products"]
    reps = tables["sales_reps"]
    targets = tables["monthly_targets"]

    checks.extend(
        [
            result("no_duplicate_transaction_ids", "sales_transactions", len(sales), int(sales["transaction_id"].duplicated().sum()), "critical"),
            result("customer_ids_match_reference", "sales_transactions", len(sales), int((~sales["customer_id"].isin(customers["customer_id"])).sum()), "critical"),
            result("product_ids_match_reference", "sales_transactions", len(sales), int((~sales["product_id"].isin(products["product_id"])).sum()), "critical"),
            result("sales_rep_ids_match_reference", "sales_transactions", len(sales), int((~sales["sales_rep_id"].isin(reps["sales_rep_id"])).sum()), "critical"),
            result("revenue_values_non_negative", "sales_transactions", len(sales), int((sales[["gross_revenue", "net_revenue"]] < 0).any(axis=1).sum()), "critical"),
            result("quantity_positive_for_active_orders", "sales_transactions", len(sales), int((sales["quantity"] <= 0).sum()), "critical"),
            result("discount_rate_between_0_and_1", "sales_transactions", len(sales), int((~sales["discount_rate"].between(0, 1)).sum()), "critical"),
            result("unit_price_non_negative", "sales_transactions", len(sales), int((sales["unit_price"] < 0).sum()), "critical"),
            result("cost_non_negative", "sales_transactions", len(sales), int((sales["cost"] < 0).sum()), "critical"),
            result(
                "gross_margin_calculated_consistently",
                "sales_transactions",
                len(sales),
                int((~np.isclose(sales["gross_margin"], sales["net_revenue"] - sales["cost"], atol=0.02)).sum()),
                "critical",
            ),
            result(
                "order_date_not_after_invoice_date",
                "sales_transactions",
                len(sales),
                int((pd.to_datetime(sales["order_date"]) > pd.to_datetime(sales["invoice_date"])).sum()),
                "high",
            ),
            result("valid_order_statuses", "sales_transactions", len(sales), int((~sales["order_status"].isin(VALID_ORDER_STATUSES)).sum()), "high"),
            result("valid_customer_active_flags", "customers", len(customers), int((~customers["active_flag"].isin(VALID_ACTIVE_FLAGS)).sum()), "high"),
            result("valid_product_active_flags", "products", len(products), int((~products["active_flag"].isin(VALID_ACTIVE_FLAGS)).sum()), "high"),
            result("no_duplicate_customer_ids", "customers", len(customers), int(customers["customer_id"].duplicated().sum()), "critical"),
            result("no_duplicate_product_ids", "products", len(products), int(products["product_id"].duplicated().sum()), "critical"),
            result("target_values_non_negative", "monthly_targets", len(targets), int((targets[["revenue_target", "margin_target", "volume_target"]] < 0).any(axis=1).sum()), "high"),
        ]
    )
    return pd.DataFrame([check.__dict__ for check in checks])


def main() -> None:
    ensure_directories()
    tables = load_raw_tables()
    report = validate_tables(tables)
    output_path = AUDIT_DIR / "data_quality_report.csv"
    report.to_csv(output_path, index=False)
    failed = report[report["status"].eq("fail")]
    print(f"Wrote data quality report to {output_path}")
    if not failed.empty:
        raise ValueError(f"Data validation failed: {len(failed)} checks did not pass")


if __name__ == "__main__":
    main()
