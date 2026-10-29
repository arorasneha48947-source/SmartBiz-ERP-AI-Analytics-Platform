import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL

load_dotenv()

url = URL.create(
    "mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME")
)

engine = create_engine(url)

query = """
SELECT
    customer,
    posting_date,
    grand_total,
    outstanding_amount
FROM `tabSales Invoice`
WHERE docstatus = 1
"""

df = pd.read_sql(query, engine)

print("\n===== SMARTBIZ LIVE SALES ANALYSIS =====")

print("\nTotal Sales Revenue:")
print("₹", df["grand_total"].sum())

print("\nTotal Invoices:")
print(len(df))

print("\nOutstanding Amount:")
print("₹", df["outstanding_amount"].sum())

print("\nCustomer-wise Sales:")
print(
    df.groupby("customer")["grand_total"]
    .sum()
    .sort_values(ascending=False)
)

engine.dispose()
