from pycoingecko import CoinGeckoAPI
import pandas as pd
import numpy as np
import time
import datetime
from datetime import date, timedelta
from datetime import datetime as dt

#Initialize coingeckpo api
cg = CoinGeckoAPI()

def get_historic_btc_price(id, vs_currency):
    #Initialize today's date for future use in app
    today = datetime.date.today()
    origin_btc = pd.to_datetime('03/01/2009').date()
    n_days = (today -origin_btc).days
    historic_bitcoin_price = cg.get_coin_market_chart_by_id(id = '{}'.format(id),
    vs_currency = '{}'.format(vs_currency), days = '{}'.format(n_days))
    historic_bitcoin_price = pd.DataFrame(historic_bitcoin_price)
    #tidy price column and extract timestamp
    prices = historic_bitcoin_price.prices.astype(str)
    prices = prices.str.split(',', expand=True)
    prices.columns = ['timestamp', 'price']
    prices['timestamp'] = prices.timestamp.str.replace('[', '')
    prices['timestamp'] = prices.timestamp.apply(lambda x: x[:-3])
    prices['price'] = prices.price.str.replace(']', '')
    prices['price'] = prices.price.astype(float)

    #tidy market_caps column and remove timestamp
    market_caps = historic_bitcoin_price.market_caps.astype(str)
    market_caps = market_caps.str.split(',', expand=True)
    market_caps.columns = ['timestamp', 'market_cap']
    market_caps = market_caps.drop('timestamp', axis =1)
    market_caps['market_cap'] = market_caps.market_cap.str.replace(']', '')
    market_caps['market_cap'] = market_caps['market_cap'].replace(' None', np.NaN)
    market_caps['market_cap'] = market_caps['market_cap'].fillna('0.0').astype(float)
    market_caps['market_cap'] = market_caps['market_cap'].fillna(method ='bfill')


    #tidy total_volume column and remove timestamp
    total_volume = historic_bitcoin_price.total_volumes.astype(str)
    total_volume = total_volume.str.split(',', expand=True)
    total_volume.columns = ['timestamp', 'total_volume']
    total_volume = total_volume.drop('timestamp', axis =1)
    total_volume['total_volume'] = total_volume.total_volume.str.replace(']', '')
    total_volume['total_volume'] = total_volume['total_volume'].replace(' None', np.NaN)
    total_volume['total_volume'] = total_volume['total_volume'].fillna('0.0').astype(float)
    total_volume['total_volume'] = total_volume['total_volume'].fillna(method ='bfill')

    #concat price, market_caps and total_volume column and drop doplicates
    historic_btc_price = pd.concat([prices, market_caps, total_volume], axis = 1).drop_duplicates()
    #tidy date column
    historic_btc_price['timestamp'] = historic_btc_price.timestamp.astype(int)
    historic_btc_price['date'] = pd.to_datetime(historic_btc_price.timestamp, unit='s')
    historic_btc_price['day'] = historic_btc_price.date.dt.day
    historic_btc_price['month'] = historic_btc_price.date.dt.month
    historic_btc_price['year'] = historic_btc_price.date.dt.year
    historic_btc_price['date_clean'] = historic_btc_price.date.dt.date
    #prepare data for analysis by setting the date column to datetime index
    historic_btc_price['date_clean'] = pd.to_datetime(historic_btc_price.date_clean)
    historic_btc_price = historic_btc_price.set_index('date_clean')
    historic_btc_price['day_of_week'] = historic_btc_price.date.dt.day_name()

    return historic_btc_price
historic_btc_price = get_historic_btc_price('bitcoin', 'gbp')
print('----------DataFrame-----------')
print(historic_btc_price.head())
print('----------Columns in dataframe-------------')
print(historic_btc_price.columns)
