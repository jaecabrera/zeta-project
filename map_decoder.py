import pandas as pd
import janitor


df = pd.read_csv('map_encoder.csv')
df = df.set_index(df.columns[0])
