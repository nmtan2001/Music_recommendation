import pandas as pd

# Read the CSV files into DataFrames
df1 = pd.read_csv('dftest.csv')
df2 = pd.read_csv('df1.csv')

# Concatenate the DataFrames
df_merged = pd.concat([df1, df2], ignore_index=True)

# Save the merged DataFrame to a new CSV file
df_merged.to_csv('merged_file.csv', index=False)
