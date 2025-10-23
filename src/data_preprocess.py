import pandas as pd
import yfinance as yf
from datetime import date, timedelta
import os

# --- Configuration ---
ticker = "GC=F"
file_path = os.path.join("data", "gold_data.xlsx")
os.makedirs("data", exist_ok=True)  # ensure data folder exists

# --- Fetch full history (if needed) ---
gold = yf.Ticker(ticker)
df = gold.history(start="2020-01-01", interval="1d")

# --- Fetch today's rate ---
today = date.today()
tomorrow = today + timedelta(days=1)
latest_price = gold.history(start=today, end=tomorrow)

# --- Remove timezone info (important for Excel) ---
df = df.reset_index()
df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)

latest_price = latest_price.reset_index()
latest_price["Date"] = pd.to_datetime(latest_price["Date"]).dt.tz_localize(None)

# --- Save or update Excel file ---
if not os.path.exists(file_path):
    df.to_excel(file_path, index=False)
    print("✅ File created successfully.")
else:
    existing_df = pd.read_excel(file_path)
    updated_df = pd.concat([existing_df, latest_price], ignore_index=True)
    updated_df.drop_duplicates(subset=["Date"], keep="last", inplace=True)
    updated_df.to_excel(file_path, index=False)
    print("✅ File updated successfully.")
