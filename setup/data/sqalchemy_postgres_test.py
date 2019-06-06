import sqlalchemy
import json, requests
import numpy as np
import pandas as pd

API_KEY = 'JRLUCAS'

def get_price_history(symbols):
    candle_list = []
    df_dict = {}
    for symbol in symbols:
        API_URL = r'https://api.tdameritrade.com/v1/marketdata/{}/pricehistory'.format(symbol)
        params = {
            'apikey': API_KEY,
            'periodType': 'month',
            'period': 1,
            'frequencyType': 'daily',
            'frequency': 1,
            'needExtendedHoursData': 'false'
        }

        content = requests.get(url=(API_URL),params=params).text

        data = json.loads(content)
        candle_list.append(data)
        for i in candle_list:
            df = pd.DataFrame.from_dict(i['candles'])
            df_dict[symbol] = df
    return df_dict

etf_list = ['VTI','VEA', 'VWO', 'VNQ', 'XLE', 'BND', 'SCHP', 'VTEB', 'VIG']

df = get_price_history(etf_list)

engine = sqlalchemy.create_engine("postgresql://app_user:password@localhost/price_test")
con = engine.connect()

table_name = 'load_data_test'
df.to_sql(table_name, con)
