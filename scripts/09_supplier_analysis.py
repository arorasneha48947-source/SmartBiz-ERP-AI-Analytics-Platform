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
    supplier,
    COUNT(name) AS total_bills,
    SUM(grand_total) AS total_purchase
FROM `tabPurchase Invoice`
WHERE docstatus = 1
GROUP BY supplier
ORDER BY total_purchase DESC
"""

df = pd.read_sql(query, engine)
engine.dispose()

print("\n===== SMARTBIZ SUPPLIER ANALYSIS =====")
print(df.to_string(index=False))

print("\nTotal Suppliers:", df["supplier"].nunique())
print("Total Purchase Amount: ₹", df["total_purchase"].sum())

df.to_excel(
    "data/processed/SmartBiz_Supplier_Report.xlsx",
    index=False
)

print("\nSupplier Excel report created successfully!")
