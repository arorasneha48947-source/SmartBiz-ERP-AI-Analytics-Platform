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

# Sales KPIs
sales = pd.read_sql("""
SELECT
    COUNT(*) AS total_invoices,
    COALESCE(SUM(grand_total), 0) AS total_revenue,
    COALESCE(SUM(outstanding_amount), 0) AS outstanding_amount
FROM `tabSales Invoice`
WHERE docstatus = 1
""", engine)

# Inventory KPIs
inventory = pd.read_sql("""
SELECT
    COUNT(DISTINCT item_code) AS total_products,
    COALESCE(SUM(actual_qty), 0) AS total_stock,
    COALESCE(SUM(stock_value), 0) AS stock_value
FROM `tabBin`
""", engine)

# Purchase KPIs
purchase = pd.read_sql("""
SELECT
    COUNT(*) AS total_bills,
    COALESCE(SUM(grand_total), 0) AS total_purchase
FROM `tabPurchase Invoice`
WHERE docstatus = 1
""", engine)

engine.dispose()

# Combine all KPIs
dashboard = pd.DataFrame([
    ["Total Sales Revenue", sales.iloc[0]["total_revenue"]],
    ["Total Sales Invoices", sales.iloc[0]["total_invoices"]],
    ["Outstanding Amount", sales.iloc[0]["outstanding_amount"]],
    ["Total Products", inventory.iloc[0]["total_products"]],
    ["Total Stock Quantity", inventory.iloc[0]["total_stock"]],
    ["Total Stock Value", inventory.iloc[0]["stock_value"]],
    ["Total Purchase Bills", purchase.iloc[0]["total_bills"]],
    ["Total Purchase Amount", purchase.iloc[0]["total_purchase"]]
], columns=["Business KPI", "Value"])

os.makedirs("data/processed", exist_ok=True)

file_path = "data/processed/SmartBiz_Business_KPI_Dashboard.xlsx"

with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
    dashboard.to_excel(writer, sheet_name="Business Dashboard", index=False)

print("\n===== SMARTBIZ BUSINESS KPI DASHBOARD =====")
print(dashboard.to_string(index=False))
print("\nDashboard created successfully!")
print("File:", file_path)
