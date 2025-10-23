import pandas as pd
import yfinance as yf
from  datetime import date, timedelta
import os

ticker = "GC=F"
gold = yf.Ticker(ticker)
df = gold.history(start="2020-01-01", interval="1d")

# Getting today's rates
today = date.today()
tomorrow  = today + timedelta(days=1)
latest_price = gold.history(start=today,end=tomorrow)


# Note if we don't remove timezone then excel won't be able to save it
df["Date"]=df.index
df['Date'] = df['Date'].dt.tz_localize(None)


# Exporting data to excel file
# File path
file_path = "data\\gold_data.xlsx"

# Export to Excel
if not os.path.exists(file_path):
    df.to_excel(file_path, index=False)  # creates file
else:
    # Append new data without overwriting the latest data record
    record = latest_price
    for col in record.select_dtypes(include=['datetime64[ns, UTC]']):
      record[col] = record[col].dt.tz_localize(None)
    existing_df = pd.read_excel(file_path)
    updated_df = pd.concat([existing_df, record], ignore_index=True)
    updated_df.to_excel(file_path, index=False)