"""Streamlit executive dashboard for the synthetic sales analytics workflow."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "output" / "reports"
POWERBI_PATH = ROOT / "output" / "powerbi" / "powerbi_sales_dashboard.csv"


@st.cache_data
def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def money(value: float) -> str:
    return f"EUR {value:,.0f}"


def pct(value: float) -> str:
    return f"{value:.1%}"


def load_dashboard_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if not POWERBI_PATH.exists():
        st.error("Run the pipeline first to create the BI-ready export.")
        st.stop()
    dashboard = load_csv(POWERBI_PATH)
    monthly = load_csv(REPORTS_DIR / "monthly_sales_summary.csv")
    customers = load_csv(REPORTS_DIR / "customer_sales_summary.csv")
    products = load_csv(REPORTS_DIR / "product_sales_summary.csv")
    regions = load_csv(REPORTS_DIR / "region_sales_summary.csv")
    return dashboard, monthly, customers, products, regions


def filter_dashboard(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filters")
    months = sorted(df["clean order month"].dropna().unique())
    selected_months = st.sidebar.multiselect("Month", months, default=months[-6:])
    regions = st.sidebar.multiselect("Region", sorted(df["region"].dropna().unique()), default=sorted(df["region"].dropna().unique()))
    categories = st.sidebar.multiselect(
        "Product category",
        sorted(df["product category"].dropna().unique()),
        default=sorted(df["product category"].dropna().unique()),
    )
    segments = st.sidebar.multiselect(
        "Customer segment",
        sorted(df["customer segment"].dropna().unique()),
        default=sorted(df["customer segment"].dropna().unique()),
    )
    return df[
        df["clean order month"].isin(selected_months)
        & df["region"].isin(regions)
        & df["product category"].isin(categories)
        & df["customer segment"].isin(segments)
    ].copy()


def kpi_cards(df: pd.DataFrame) -> None:
    closed = df[df["dashboard order status"].eq("Closed")]
    total_revenue = closed["net revenue"].sum()
    gross_margin = closed["gross margin"].sum()
    orders = closed["transaction id"].nunique()
    active_customers = closed["customer id"].nunique()
    target_rate = (closed["net revenue"].sum() / closed["revenue target"].sum()) if closed["revenue target"].sum() else 0
    columns = st.columns(6)
    columns[0].metric("Net revenue", money(total_revenue))
    columns[1].metric("Gross margin", money(gross_margin))
    columns[2].metric("Margin %", pct(gross_margin / total_revenue if total_revenue else 0))
    columns[3].metric("Orders", f"{orders:,}")
    columns[4].metric("Customers", f"{active_customers:,}")
    columns[5].metric("Target rate", pct(target_rate))


def main() -> None:
    st.set_page_config(page_title="Sales Performance Dashboard", layout="wide")
    st.title("Sales Performance Dashboard")
    st.caption("Synthetic sales dataset | simulated business case | BI-ready output")

    dashboard, monthly, customers, products, regions = load_dashboard_data()
    filtered = filter_dashboard(dashboard)
    kpi_cards(filtered)

    tabs = st.tabs(
        [
            "Executive Overview",
            "Revenue & Margin",
            "Product Performance",
            "Customer Performance",
            "Region & Channel",
            "Target Achievement",
            "Data Quality / Methodology",
        ]
    )

    with tabs[0]:
        st.subheader("Management view")
        st.line_chart(monthly.set_index("reporting_month")[["net_revenue", "gross_margin"]])
        st.dataframe(monthly.tail(12), use_container_width=True, hide_index=True)

    with tabs[1]:
        left, right = st.columns(2)
        revenue_by_channel = filtered.groupby("channel", as_index=True)["net revenue"].sum().sort_values(ascending=False)
        margin_by_category = filtered.groupby("product category", as_index=True)["gross margin"].sum().sort_values(ascending=False)
        left.subheader("Revenue by channel")
        left.bar_chart(revenue_by_channel)
        right.subheader("Margin by product category")
        right.bar_chart(margin_by_category)
        st.subheader("Discount impact")
        st.bar_chart(filtered.groupby("clean order month")["discount amount"].sum())

    with tabs[2]:
        st.subheader("Product performance bands")
        st.dataframe(products.sort_values("total_revenue", ascending=False), use_container_width=True, hide_index=True)
        st.bar_chart(products.set_index("product_name")["total_revenue"].sort_values(ascending=False).head(10))

    with tabs[3]:
        st.subheader("Top customers")
        st.dataframe(customers.sort_values("total_revenue", ascending=False).head(20), use_container_width=True, hide_index=True)
        st.bar_chart(customers.groupby("customer_value_band")["total_revenue"].sum().sort_values(ascending=False))

    with tabs[4]:
        st.subheader("Region and channel analysis")
        st.dataframe(regions.sort_values("total_revenue", ascending=False), use_container_width=True, hide_index=True)
        st.bar_chart(filtered.groupby("region")["net revenue"].sum().sort_values(ascending=False))
        st.subheader("Sales rep ranking")
        reps = filtered.groupby(["sales rep id", "sales rep name"], as_index=False)["net revenue"].sum()
        st.dataframe(reps.sort_values("net revenue", ascending=False), use_container_width=True, hide_index=True)

    with tabs[5]:
        target_view = monthly[["reporting_month", "net_revenue", "revenue_target", "target_achievement_rate"]].copy()
        st.subheader("Revenue vs target")
        st.line_chart(target_view.set_index("reporting_month")[["net_revenue", "revenue_target"]])
        st.dataframe(target_view.tail(12), use_container_width=True, hide_index=True)

    with tabs[6]:
        st.subheader("Methodology")
        st.info(
            "This Streamlit demo uses a synthetic sales dataset. The workflow validates raw files, enriches transactions, "
            "calculates KPI tables, and exports a flat BI-ready dataset for dashboarding."
        )
        quality_path = ROOT / "output" / "audit" / "data_quality_report.csv"
        if quality_path.exists():
            st.dataframe(load_csv(quality_path), use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
