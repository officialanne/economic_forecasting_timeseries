import pandas as pd
from pathlib import Path

# file paths
project_root = Path(__file__).parent.parent
raw_path = project_root / "data" / "raw" / "raw_uk_cpi.csv"
processed_path = project_root / "data" / "processed" / "uk_cpi_clean.csv"

# load raw data
df = pd.read_csv(raw_path)

# rename columns
df = df.rename(columns={'Title': 'Date', 'CPIH ANNUAL RATE 00: ALL ITEMS 2015=100': 'Inflation'})

# create boolean mask
month_mask = df["Date"].str.contains("JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC")

# create dataframe with monthly data only
month_df = df[month_mask]

# create a copy of the monthly df
clean_df = month_df.copy()

# convert inflation column to float
clean_df["Inflation"] = clean_df["Inflation"].astype(float)

# convert data column to datetime
clean_df["Date"] = pd.to_datetime(clean_df["Date"], format="%Y %b")

# set the date column to be the index
clean_df = clean_df.set_index("Date")

if (clean_df.index.is_monotonic_increasing):
    clean_df.to_csv(processed_path)