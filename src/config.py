"""Shared project configuration for the sales analytics workflow."""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
REFERENCE_DIR = DATA_DIR / "reference"
OUTPUT_DIR = ROOT_DIR / "output"
REPORTS_DIR = OUTPUT_DIR / "reports"
POWERBI_DIR = OUTPUT_DIR / "powerbi"
AUDIT_DIR = OUTPUT_DIR / "audit"
SCREENSHOTS_DIR = ROOT_DIR / "screenshots"

RANDOM_SEED = 5050
CURRENCY = "EUR"

VALID_ORDER_STATUSES = {"Invoiced", "Shipped", "Open", "Cancelled"}
VALID_CHANNELS = {"Direct", "Partner", "Distributor", "Online"}
VALID_ACTIVE_FLAGS = {"Y", "N"}


def ensure_directories() -> None:
    """Create the folder structure used by the pipeline."""
    for path in [
        RAW_DIR,
        PROCESSED_DIR,
        REFERENCE_DIR,
        REPORTS_DIR,
        POWERBI_DIR,
        AUDIT_DIR,
        SCREENSHOTS_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)
