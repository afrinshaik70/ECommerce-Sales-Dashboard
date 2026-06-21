
import pandas as pd
import os

# Load data correctly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "sales.csv")

df = pd.read_csv(DATA_PATH)

# ================= KPIs =================
def get_kpis():
    return {
        "total_sales": df["Sales"].sum(),
        "total_profit": df["Profit"].sum(),
        "total_orders": df["Order_ID"].nunique()
    }

# ================= CATEGORY =================
def category_sales():
    return df.groupby("Category")["Sales"].sum().reset_index()

# ================= STATE =================
def state_sales():
    return df.groupby("State")["Sales"].sum().reset_index()

# ================= TOP PRODUCTS =================
def top_products():
    return (
        df.groupby("Product_Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

# ================= SALES TREND =================
def sales_trend():
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df.groupby("Order_Date")["Sales"].sum().reset_index()