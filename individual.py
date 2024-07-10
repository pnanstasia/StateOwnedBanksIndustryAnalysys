import pandas as pd
import numpy as np  # Import numpy for NaN handling

def calculate_CR(number_of_banks):
    df = pd.read_csv('data/original/TA.csv')

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    df['total'] = df[numeric_cols].sum(axis=1)

    for i in range(len(df)):
        total_value = df.at[i, 'total']
        for col in numeric_cols:
            df.at[i, col] = df.at[i, col] / total_value

    top_values = []

    for i in range(len(df)):
        row = df.iloc[i]
        sorted_row = row[numeric_cols].sort_values(ascending=False)
        top_values.append(sorted_row[:number_of_banks])

    return top_values

print(calculate_CR(10))
