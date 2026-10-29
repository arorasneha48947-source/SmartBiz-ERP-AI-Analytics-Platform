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
    item_code,
    warehouse,
    actual_qty,
    stock_value
FROM `tabBin`
"""

df = pd.read_sql(query, engine)
engine.dispose()

print("\n===== SMARTBIZ INVENTORY ANALYSIS =====")
print(df.to_string(index=False))

print("\nTotal Products:", df["item_code"].nunique())
print("Total Stock Quantity:", df["actual_qty"].sum())
print("Total Stock Value: ₹", df["stock_value"].sum())

df.to_excel(
    "data/processed/SmartBiz_Inventory_Report.xlsx",
    index=False
)

print("\nInventory Excel report created successfully!")
