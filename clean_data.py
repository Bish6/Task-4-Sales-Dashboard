from pathlib import Path
import pandas as pd

# Find the project folder and the original CSV file.
project_folder = Path(__file__).parent
raw_file = project_folder / "data" / "SuperStoreOrders - SuperStoreOrders.csv"

# Read the CSV.
df = pd.read_csv(raw_file)

print("Original rows and columns:", df.shape)

# Tidy up spaces in column names and text values.
df.columns = df.columns.str.strip()

for column in df.select_dtypes(include="object").columns:
    df[column] = df[column].str.strip()

# Convert the date columns into real dates.
# These dates are written as month/day/year, such as 1/2/2011.
for column in ["order_date", "ship_date"]:
    df[column] = pd.to_datetime(
        df[column],
        format="%d/%m/%Y",
        errors="coerce"
    )

# Convert these columns from text to numbers.
number_columns = [
    "sales",
    "quantity",
    "discount",
    "profit",
    "shipping_cost",
    "year"
]

for column in number_columns:
    df[column] = pd.to_numeric(
        df[column].astype(str).str.replace(",", "", regex=False),
        errors="coerce"
    )

# Remove only rows that are exact copies of another row.
before_duplicates = len(df)
df = df.drop_duplicates()
duplicates_removed = before_duplicates - len(df)

# Remove rows missing information needed for the dashboard.
important_columns = [
    "order_date",
    "sales",
    "profit",
    "category",
    "region"
]

before_missing = len(df)
df = df.dropna(subset=important_columns)
missing_rows_removed = before_missing - len(df)

# Add a month-start date for the monthly sales chart.
df["order_month"] = (
    df["order_date"]
    .dt.to_period("M")
    .dt.to_timestamp()
)

# Save the cleaned copy beside the original CSV.
clean_file = project_folder / "data" / "superstore_clean.csv"
df.to_csv(clean_file, index=False)

# Print a simple cleaning report.
print("Exact duplicate rows removed:", duplicates_removed)
print("Rows missing important values removed:", missing_rows_removed)
print("Cleaned rows and columns:", df.shape)
print("Cleaned file saved to:", clean_file)
print("Cleaning complete.")