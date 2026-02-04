
# libs
import pandas as pd
import requests
from Pygs import Pygs # Notice how the class is acting lke a libraby!

# ----------------------
# This script pulls data from an api, normalizes it if needed, filters and stores in google sheets.

response = requests.get("https://fakestoreapi.com/products")
df = pd.DataFrame(response.json())
# df = pd.json_normalize(df)  # use if the data you pull data within data
df = df[df['price']> 10].copy() # filtering of irrelevant data

summary = df.groupby(['category']).agg(
            {
            'id': 'nunique',      # Count unique items
            'price': 'sum'        # Sum of prices (Revenue)
            }
        )

summary = summary.reset_index()
summary.columns = ['Category', 'Product Count', 'Total Potential Revenue']

pg = Pygs(spreadsheet_id='1UUtUT06eVcxj4CfMGHdZKJWxIcIyYZINXJzid8J_wO4')

pg.create_sheet('data pull')
pg.dataframe_to_sheet(sheet_name='data pull',dataframe=summary)


