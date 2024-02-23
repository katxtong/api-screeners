import json
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from requests import Request, Session
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from pandas import json_normalize

api = "72bff5eb-7918-4881-aeb1-ef6addf6027e"


url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '3000',
    'limit': '5000',
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api,
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    df = pd.DataFrame(data['data'])
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

platform = json_normalize(df['platform'])
platform.columns = ['platform_id', 'platform_name',
                    'platform_symbol', 'platform_slug', 'platform_token_address']
df_all = pd.concat([df, platform, json_normalize(df['quote'])], axis=1)
df.drop(columns=['quote', 'platform'], inplace=True)
df_all.to_csv("top5000_cmc.csv")
