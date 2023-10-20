import pandas as pd
import numpy as np

df = pd.read_csv("df.csv")
df.drop(columns='Unnamed: 0', inplace=True)

# Dataframe for getting year feature of songs
dfYear = pd.read_csv("dfYear.csv")

# Merge 2 Dataframe
df = pd.merge(df, dfYear, on='track_id')
df.to_csv('final.csv', index=False)

print(df)
