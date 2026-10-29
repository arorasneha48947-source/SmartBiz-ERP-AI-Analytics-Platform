import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL, text

# Load database settings
load_dotenv()

# Read credentials
connection_url = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME")
)

# Create database connection
engine = create_engine(connection_url)

# Test connection
with engine.connect() as connection:
    result = connection.execute(text(
        "SELECT COUNT(*) FROM `tabSales Invoice`"
    ))
    count = result.scalar()

print("ERPNext database connected successfully!")
print("Total Sales Invoices:", count)

# Read data using Pandas
df = pd.read_sql(
    "SELECT name, customer, posting_date, grand_total "
    "FROM `tabSales Invoice`",
    engine
)

print("\nSales Invoice Data:")
print(df.to_string(index=False))

engine.dispose()
