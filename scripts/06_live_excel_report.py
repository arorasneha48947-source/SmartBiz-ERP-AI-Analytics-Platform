import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL
from openpyxl.styles import Font, PatternFill, Alignment

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
    name AS Invoice_ID,
    customer AS Customer,
    posting_date AS Invoice_Date,
    grand_total AS Sales_Amount,
    outstanding_amount AS Outstanding_Amount
FROM `tabSales Invoice`
WHERE docstatus = 1
"""

df = pd.read_sql(query, engine)
engine.dispose()

summary = pd.DataFrame({
    "KPI": ["Total Revenue", "Total Invoices", "Outstanding Amount"],
    "Value": [
        df["Sales_Amount"].sum(),
        len(df),
        df["Outstanding_Amount"].sum()
    ]
})

file_path = "data/processed/SmartBiz_Live_Sales_Report.xlsx"

with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Sales Data", index=False)
    summary.to_excel(writer, sheet_name="KPI Summary", index=False)

    for sheet in writer.book.worksheets:
        sheet.freeze_panes = "A2"
        for cell in sheet[1]:
            cell.fill = PatternFill(
                start_color="17365D",
                end_color="17365D",
                fill_type="solid"
            )
            cell.font = Font(color="FFFFFF", bold=True)
            cell.alignment = Alignment(horizontal="center")

        for column in sheet.columns:
            max_length = max(
                len(str(cell.value or "")) for cell in column
            )
            sheet.column_dimensions[column[0].column_letter].width = max_length + 4

print("Live ERPNext Excel report created successfully!")
print("File:", file_path)
print("Total Revenue: ₹", df["Sales_Amount"].sum())
