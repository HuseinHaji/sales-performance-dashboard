"""Generate a deterministic synthetic B2B sales dataset for portfolio analysis."""

from __future__ import annotations

import numpy as np
import pandas as pd

from config import CURRENCY, RANDOM_SEED, RAW_DIR, ensure_directories


REGIONS = {
    "DACH": ["Germany", "Austria", "Switzerland"],
    "Northern Europe": ["Netherlands", "Sweden", "Denmark"],
    "Western Europe": ["France", "Belgium", "Ireland"],
    "Southern Europe": ["Spain", "Italy", "Portugal"],
}

INDUSTRIES = ["Manufacturing", "Technology", "Retail", "Healthcare", "Logistics", "Professional Services"]
SEGMENTS = ["Enterprise", "Mid-Market", "SMB"]
COMPANY_SIZES = ["51-200", "201-500", "501-1000", "1001-5000", "5000+"]
CHANNELS = ["Direct", "Partner", "Distributor", "Online"]


def generate_calendar() -> pd.DataFrame:
    dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")
    return pd.DataFrame(
        {
            "date": dates.date,
            "month": dates.to_period("M").astype(str),
            "quarter": "Q" + dates.quarter.astype(str),
            "year": dates.year,
            "month_name": dates.strftime("%B"),
        }
    )


def generate_customers(rng: np.random.Generator, count: int = 90) -> pd.DataFrame:
    rows = []
    region_names = list(REGIONS)
    for index in range(1, count + 1):
        region = rng.choice(region_names, p=[0.38, 0.22, 0.24, 0.16])
        country = rng.choice(REGIONS[region])
        rows.append(
            {
                "customer_id": f"CUST{index:04d}",
                "customer_name": f"{rng.choice(['Apex', 'Nexa', 'Urban', 'Prime', 'Vertex', 'Helio'])} {index:03d} GmbH",
                "country": country,
                "region": region,
                "industry": rng.choice(INDUSTRIES),
                "company_size": rng.choice(COMPANY_SIZES, p=[0.18, 0.25, 0.24, 0.22, 0.11]),
                "customer_segment": rng.choice(SEGMENTS, p=[0.22, 0.48, 0.30]),
                "onboarding_date": pd.Timestamp("2020-01-01") + pd.Timedelta(days=int(rng.integers(0, 1800))),
                "active_flag": rng.choice(["Y", "N"], p=[0.92, 0.08]),
            }
        )
    return pd.DataFrame(rows)


def generate_products() -> pd.DataFrame:
    products = [
        ("PRD001", "Analytics Platform Pro", "Software", "Performance Management", 4600, 8200),
        ("PRD002", "Sales Planning Suite", "Software", "Planning", 3900, 7600),
        ("PRD003", "Integration Connector Pack", "Software", "Data Integration", 900, 2100),
        ("PRD004", "Industrial Sensor Kit", "Hardware", "Monitoring", 620, 1450),
        ("PRD005", "Edge Control Unit", "Hardware", "Automation", 2100, 4300),
        ("PRD006", "Field Service Package", "Services", "Implementation", 1200, 2600),
        ("PRD007", "Managed Support Contract", "Services", "Support", 850, 1900),
        ("PRD008", "Commercial Intelligence Workshop", "Services", "Advisory", 1800, 3600),
        ("PRD009", "Energy Optimization Module", "Industrial", "Efficiency", 2800, 5900),
        ("PRD010", "Production Quality Module", "Industrial", "Quality", 2500, 5400),
        ("PRD011", "Customer Portal License", "Software", "Portal", 1300, 3200),
        ("PRD012", "Installation Hardware Bundle", "Hardware", "Installation", 780, 1700),
    ]
    return pd.DataFrame(
        products,
        columns=["product_id", "product_name", "product_category", "product_family", "unit_cost", "list_price"],
    ).assign(active_flag="Y")


def generate_sales_reps(rng: np.random.Generator) -> pd.DataFrame:
    names = [
        "Anna Weber",
        "Lukas Schneider",
        "Mara Hoffmann",
        "Jonas Becker",
        "Sofia Klein",
        "David Fischer",
        "Elena Wagner",
        "Noah Meyer",
        "Clara Richter",
        "Felix Bauer",
        "Laura Schmitt",
        "Tim Keller",
    ]
    teams = ["Enterprise", "Mid-Market", "Commercial"]
    rows = []
    for index, name in enumerate(names, start=1):
        region = list(REGIONS)[(index - 1) % len(REGIONS)]
        rows.append(
            {
                "sales_rep_id": f"REP{index:03d}",
                "sales_rep_name": name,
                "team": rng.choice(teams),
                "region": region,
                "manager": rng.choice(["Nina Hartmann", "Markus Vogel", "Sarah Brandt"]),
                "hire_date": pd.Timestamp("2019-01-01") + pd.Timedelta(days=int(rng.integers(0, 1700))),
            }
        )
    return pd.DataFrame(rows)


def generate_transactions(
    rng: np.random.Generator, customers: pd.DataFrame, products: pd.DataFrame, reps: pd.DataFrame
) -> pd.DataFrame:
    rows = []
    months = pd.date_range("2024-01-01", "2025-12-01", freq="MS")
    status_choices = ["Invoiced", "Shipped", "Open", "Cancelled"]
    status_probability = [0.74, 0.17, 0.07, 0.02]
    transaction_number = 1

    for month_index, month_start in enumerate(months):
        seasonal_multiplier = 1.0 + (0.16 if month_start.month in [3, 6, 9, 11] else 0.0)
        trend_multiplier = 1.0 + month_index * 0.012
        orders = int(rng.integers(115, 155) * seasonal_multiplier)
        for _ in range(orders):
            customer = customers.sample(1, random_state=int(rng.integers(1_000_000))).iloc[0]
            product = products.sample(1, random_state=int(rng.integers(1_000_000))).iloc[0]
            rep_pool = reps[reps["region"].eq(customer["region"])]
            rep = rep_pool.sample(1, random_state=int(rng.integers(1_000_000))).iloc[0]
            order_date = month_start + pd.Timedelta(days=int(rng.integers(0, 27)))
            invoice_date = order_date + pd.Timedelta(days=int(rng.integers(0, 10)))
            quantity = int(rng.integers(1, 9))
            discount_rate = round(float(rng.beta(2, 12) * 0.35), 3)
            if customer["customer_segment"] == "Enterprise":
                quantity += int(rng.integers(2, 8))
                discount_rate = min(discount_rate + 0.035, 0.45)
            unit_price = round(float(product["list_price"] * rng.uniform(0.94, 1.08) * trend_multiplier), 2)
            gross_revenue = round(quantity * unit_price, 2)
            net_revenue = round(gross_revenue * (1 - discount_rate), 2)
            cost = round(quantity * float(product["unit_cost"]) * rng.uniform(0.96, 1.08), 2)
            status = rng.choice(status_choices, p=status_probability)
            if status == "Cancelled":
                gross_revenue = net_revenue = cost = 0.0
            gross_margin = round(net_revenue - cost, 2)
            rows.append(
                {
                    "transaction_id": f"TXN{transaction_number:06d}",
                    "customer_id": customer["customer_id"],
                    "product_id": product["product_id"],
                    "sales_rep_id": rep["sales_rep_id"],
                    "channel": rng.choice(CHANNELS, p=[0.46, 0.27, 0.18, 0.09]),
                    "order_date": order_date.date(),
                    "invoice_date": invoice_date.date(),
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "discount_rate": round(discount_rate, 3),
                    "gross_revenue": gross_revenue,
                    "net_revenue": net_revenue,
                    "cost": cost,
                    "gross_margin": gross_margin,
                    "currency": CURRENCY,
                    "order_status": status,
                }
            )
            transaction_number += 1
    return pd.DataFrame(rows)


def generate_targets(rng: np.random.Generator, transactions: pd.DataFrame, customers: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    enriched = transactions.merge(customers[["customer_id", "region"]], on="customer_id").merge(
        products[["product_id", "product_category"]], on="product_id"
    )
    enriched["month"] = pd.to_datetime(enriched["order_date"]).dt.to_period("M").astype(str)
    base = (
        enriched[enriched["order_status"].ne("Cancelled")]
        .groupby(["month", "region", "product_category", "sales_rep_id"], as_index=False)
        .agg(net_revenue=("net_revenue", "sum"), gross_margin=("gross_margin", "sum"), quantity=("quantity", "sum"))
    )
    base["revenue_target"] = (base["net_revenue"] * rng.uniform(0.94, 1.13, len(base))).round(2)
    base["margin_target"] = (base["gross_margin"] * rng.uniform(0.93, 1.12, len(base))).round(2)
    base["volume_target"] = np.maximum(1, (base["quantity"] * rng.uniform(0.92, 1.10, len(base))).round(0)).astype(int)
    return base[["month", "region", "product_category", "sales_rep_id", "revenue_target", "margin_target", "volume_target"]]


def main() -> None:
    ensure_directories()
    rng = np.random.default_rng(RANDOM_SEED)
    customers = generate_customers(rng)
    products = generate_products()
    reps = generate_sales_reps(rng)
    calendar = generate_calendar()
    transactions = generate_transactions(rng, customers, products, reps)
    targets = generate_targets(rng, transactions, customers, products)

    customers.to_csv(RAW_DIR / "customers.csv", index=False)
    products.to_csv(RAW_DIR / "products.csv", index=False)
    reps.to_csv(RAW_DIR / "sales_reps.csv", index=False)
    calendar.to_csv(RAW_DIR / "calendar.csv", index=False)
    transactions.to_csv(RAW_DIR / "sales_transactions.csv", index=False)
    targets.to_csv(RAW_DIR / "monthly_targets.csv", index=False)
    print(f"Generated synthetic sales dataset in {RAW_DIR}")


if __name__ == "__main__":
    main()
