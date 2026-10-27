import pandas as pd
import matplotlib.pyplot as plt

# Sales & Revenue Analysis
df = pd.read_csv("sales_data.csv")
df["Date"] = pd.to_datetime(df["Date"])

print("SALES & REVENUE ANALYSIS")
print("=" * 40)
print(f"Total Sales: ₹{df['Sales'].sum():,.2f}")
print(f"Total Profit: ₹{df['Profit'].sum():,.2f}")
print(f"Total Quantity Sold: {df['Quantity'].sum():,}")
print(f"Number of Orders: {df['Order_ID'].nunique():,}")
print(f"Average Order Value: ₹{df['Sales'].mean():,.2f}")

print("\nTop Products by Sales:")
print(df.groupby("Product")["Sales"].sum().sort_values(ascending=False))

print("\nSales by Region:")
print(df.groupby("Region")["Sales"].sum().sort_values(ascending=False))

monthly = df.groupby(df["Date"].dt.to_period("M"))["Sales"].sum()

plt.figure(figsize=(10, 5))
monthly.plot(marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
