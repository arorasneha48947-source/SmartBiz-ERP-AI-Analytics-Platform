import os
import pandas as pd
import matplotlib.pyplot as plt
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
SELECT customer, SUM(grand_total) AS revenue
FROM `tabSales Invoice`
WHERE docstatus = 1
GROUP BY customer
"""

df = pd.read_sql(query, engine)
engine.dispose()

plt.figure(figsize=(9, 5))
plt.bar(df["customer"], df["revenue"])

plt.title("SmartBiz Customer-wise Sales Revenue")
plt.xlabel("Customers")
plt.ylabel("Revenue (INR)")
plt.xticks(rotation=20)
plt.tight_layout()

os.makedirs("reports", exist_ok=True)
plt.savefig("reports/customer_sales_chart.png", dpi=300)
plt.show()

print("Sales chart created successfully!")
