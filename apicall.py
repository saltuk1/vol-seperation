import csv
import time
from polygon import RESTClient
from polygon.exceptions import BadResponse
from datetime import date, timedelta, datetime
import pandas as pd

client = RESTClient("KEY") # Replace with your actual API key

ticker = 'GOOG'
start_date_str = '2024-03-01'
end_date_str = '2025-05-30'

output_csv_filename = f"{ticker}_daily_data_{start_date_str}_to_{end_date_str}.csv"

all_data_for_df = []

print(f"Fetching daily aggregates for {ticker} from {start_date_str} to {end_date_str}...")

try:
    for agg in client.list_aggs(
        ticker=ticker,
        multiplier=1,
        timespan='day',
        from_=start_date_str, # Changed 'from' to 'from_'
        to=end_date_str,
        adjusted=True
    ):
        # Explicitly ensure timestamp is a datetime object
        # The timestamp from Polygon is in milliseconds, so divide by 1000
        if isinstance(agg.timestamp, int):
            agg_datetime = datetime.fromtimestamp(agg.timestamp / 1000)
        elif isinstance(agg.timestamp, datetime):
            agg_datetime = agg.timestamp
        else:
            print(f"Warning: Unexpected type for agg.timestamp: {type(agg.timestamp)}. Skipping this aggregate.")
            continue

        row_dict = {
            'Date': agg_datetime.date().isoformat(),
            'Open': agg.open,
            'High': agg.high,
            'Low': agg.low,
            'Close': agg.close,
            'Volume': agg.volume,
            'VWAP': agg.vwap,
            'Transactions': agg.transactions,
            'Ticker': ticker
        }
        all_data_for_df.append(row_dict)
        print(agg) # This will print each aggregate object as it's fetched

except BadResponse as e:
    print(f"Error fetching data: {e.message}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# --- Save to CSV using Pandas ---
if all_data_for_df:
    column_order = [
         'Date', 'Ticker', 'Open', 'High', 'Low', 'Close',
        'Volume', 'VWAP', 'Transactions'
    ]

    df = pd.DataFrame(all_data_for_df, columns=column_order)

    try:
        df.to_csv(output_csv_filename, index=False)
        print(f"\nSuccessfully saved data to {output_csv_filename}")
    except IOError as e:
        print(f"Error writing CSV file: {e}")
else:
    print("\nNo data collected to save to CSV.")
