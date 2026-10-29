import pandas as pd

data = {
    "Product": ["Samsung Galaxy S24", "HP Laptop", "boAt Earbuds", "LG Smart TV"],
    "Category": ["Mobile", "Laptop", "Accessories", "Television"],
    "Quantity_Sold": [2, 3, 10, 1],
    "Selling_Price": [55000, 60000, 2000, 45000],
}

df = pd.DataFrame(data)

df["Total_Revenue"] = df["Quantity_Sold"] * df["Selling_Price"]

print("\nSMARTBIZ SALES DATA")
print(df)

print("\nTOTAL REVENUE:")
print(df["Total_Revenue"].sum())

print("\nTOTAL UNITS SOLD:")
print(df["Quantity_Sold"].sum())

print("\nREVENUE BY CATEGORY:")
print(df.groupby("Category")["Total_Revenue"].sum())

# Export sales data to Excel
output_file = "data/processed/smartbiz_sales_analysis.xlsx"

df.to_excel(output_file, index=False)

print("\nExcel file created successfully!")
print("Saved at:", output_file)

# Export sales data to Excel
output_file = "data/processed/smartbiz_sales_analysis.xlsx"

df.to_excel(output_file, index=False)

print("\nExcel file created successfully!")
print("Saved at:", output_file)
