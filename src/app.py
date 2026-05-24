import streamlit as st
import pandas as pd
import os


@st.cache_data
def load_data(path: str):
    return pd.read_csv(path)


DATA_PATH = os.path.join("data", "sample", "fact_sales_sample.csv")


def main():
    st.title("Sales Performance — Demo")
    df = load_data(DATA_PATH)
    st.subheader("Sample Sales")
    st.dataframe(df)
    st.subheader("Revenue by Order")
    st.bar_chart(df.set_index("order_id")["unit_price"])


if __name__ == "__main__":
    main()
