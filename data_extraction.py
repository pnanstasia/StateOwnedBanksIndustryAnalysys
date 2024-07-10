import os
import pandas as pd
import numpy as np
from datetime import datetime
from pandas.tseries.offsets import DateOffset

def extract_bank_data(root_folder, sheet_name, column, file):
    target_banks = ["privatbank", "oschadbank", "ukreximbank", "ukrgasbank", "alfa", "sense", "first investment bank"]
    data = {}

    for year in range(2020, 2025):
        folder = os.path.join(root_folder, str(year))
        if not os.path.exists(folder):
            continue

        for file_name in os.listdir(folder):
            if file_name.startswith("aggregation_") and file_name.endswith(".xlsx"):
                file_path = os.path.join(folder, file_name)
                date = datetime.strptime(file_name[12:22], "%Y-%m-%d")

                try:
                    # Try reading with 4th row as header
                    df = pd.read_excel(file_path, sheet_name=sheet_name, header=3)
                    target_col = find_target_column(df, column)

                    # If target column not found, try with 5th row as header
                    if target_col is None:
                        df = pd.read_excel(file_path, sheet_name=sheet_name, header=4)
                        target_col = find_target_column(df, column)

                    if target_col is None:
                        print(f"Warning: Target column '{column}' not found in {file_name}")
                        continue

                except Exception as e:
                    print(f"Error reading {file_name}: {str(e)}")
                    continue

                for bank in target_banks:
                    bank_row = df[df['Bank'].astype(str).str.lower().str.contains(bank, case=False, na=False)]
                    if not bank_row.empty:
                        value = bank_row[target_col].values[0]
                        if date not in data:
                            data[date] = {}
                        data[date][bank] = value

    result_df = pd.DataFrame.from_dict(data, orient='index')
    result_df.index.name = 'Date'
    result_df.sort_index(inplace=True)

    output_file = file + ".csv"
    result_df['sense'] = result_df['alfa'] + result_df['sense']
    result_df = result_df.drop(columns=['alfa'])
    result_df.to_csv(output_file)
    result_df.index = pd.to_datetime(result_df.index)


    # Shift all dates one month back
    result_df.index = result_df.index - DateOffset(months=1)
    print(f"Data extracted and saved to {output_file}")

def find_target_column(df, column):
    for col in df.columns:
        if isinstance(col, str) and column.lower() in col.lower():
            return col
    return None

# extract_bank_data('original_dataset/aggregation', 'Assets', 'Total assets', 'data/Total_Assets')

import pandas as pd
import matplotlib.pyplot as plt


def plot_donut_chart(csv_file, period, all_banks):
    # Read the CSV file
    df = pd.read_csv(csv_file, header=0, names=['date'] + [bank[0] for bank in all_banks])
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # Format the period to match the index
    period = pd.to_datetime(period).strftime('%Y-%m')

    # Check if the specified period exists in the dataframe
    if period not in df.index.strftime('%Y-%m'):
        raise ValueError(f"Period '{period}' not found in the CSV file.")

    # Extract data for the specified period
    data = df.loc[df.index.strftime('%Y-%m') == period].iloc[0]

    # Filter data and colors for banks present in the CSV
    present_banks = [bank for bank in all_banks if bank[0] in data.index]
    values = [data[bank[0]] for bank in present_banks]
    colors = [bank[1] for bank in present_banks]
    labels = [bank[0].capitalize() for bank in present_banks]

    # Create the donut chart
    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts, autotexts = ax.pie(
        values, colors=colors, labels=labels, autopct='%1.1f%%', pctdistance=0.85,
        wedgeprops=dict(width=0.5, edgecolor='white', alpha=0.5)  # Set transparency and keep edge color solid
    )

    # Add a circle at the center to create the donut shape
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)

    # Add title
    plt.title(f"Bank Distribution for {period}", fontsize=16)

    # Adjust text properties
    plt.setp(autotexts, size=8, weight="bold")
    plt.setp(texts, size=10)

    # Add legend
    ax.legend(wedges, labels, title="Banks", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    plt.tight_layout()
    plt.show()


def plot_stacked_area_chart(csv_file, list):
    # Read CSV into pandas DataFrame
    df = pd.read_csv(csv_file)

    # Set the index to the first column (date) for easier plotting
    df.set_index(df.columns[0], inplace=True)
    df.index = pd.to_datetime(df.index)

    # Plotting
    plt.figure(figsize=(10, 6))

    # Plot the stacked area with transparency
    for bank in list:
        plt.fill_between(df.index, df[bank[0]], color=bank[1], alpha=0.5, label=bank[0])
        plt.plot(df.index, df[bank[0]], color=bank[1])

    # Add labels and title
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Stacked Area Chart of Bank Balances')
    plt.legend()

    # Show plot
    plt.show()

    # Show plot
    plt.show()