import openpyxl
import pandas as pd
import os
from datetime import datetime

banks = ["privatbank", "oschadbank", "ukreximbank", "ukrgasbank", "sense", "first investment bank"]

def generate_date_range(start, end):
    """Generate a list of month-end dates from start to end."""
    date_range = pd.date_range(start=start, end=end, freq='M').strftime('%Y-%m').tolist()
    return date_range

def aggregate_data(column_name, output_csv):
    base_dir = 'original_dataset/aggregation'
    date_range = generate_date_range('2020-02', '2024-06')
    result_df = pd.DataFrame(index=date_range, columns=banks)
    for year in os.listdir(base_dir):
        year_path = os.path.join(base_dir, year)
        if os.path.isdir(year_path):
            for month_file in os.listdir(year_path):
                month_path = os.path.join(year_path, month_file)
                if month_file.endswith('.xlsx'):
                    date_str = f"{year}-{month_file.split('-')[1]}"
                    df = pd.read_excel(month_path)
                    df.columns = df.iloc[3]
                    if 1 in df.columns:
                        df.columns = df.iloc[2]
                    if df.empty or column_name not in df.columns:
                        continue
                    counter = -1
                    for bank in df["Bank"]:
                        if bank == "JSC 'ALFA-BANK'":
                            bank = "sense"
                        counter += 1
                        if not isinstance(bank, str):
                            continue
                        for bank_from_list in banks:
                            if bank_from_list in bank.lower():
                                result_df.at[date_str, bank_from_list] = df[column_name][counter]
                                break        
    result_df.to_csv(output_csv)

aggregate_data('Total assets', 'output.csv')