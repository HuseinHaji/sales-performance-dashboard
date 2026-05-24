import os


def test_sample_sales_exists():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "sample", "fact_sales_sample.csv")
    assert os.path.exists(path)
