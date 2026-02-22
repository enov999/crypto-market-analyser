import requests
import pandas as pd
import datetime

def fetchPriceHistory(coin: str, start_date: str | datetime.datetime, end_date: str | datetime.datetime, currency: str = 'gbp') -> pd.DataFrame:
    """
    Fetches historical price and volume data for a specified cryptocurrency from the CoinGecko API.

    Parameters:
    - coin (str): The cryptocurrency symbol (e.g., 'bitcoin').
    - start_date (str | datetime.datetime): The start date for the data in 'YYYY-MM-DD' format or as a datetime object.
    - end_date (str | datetime.datetime): The end date for the data in 'YYYY-MM-DD'
    - currency (str, optional): The fiat currency to compare against (e.g., 'gbp'). Default is 'gbp'.

    Returns:
    - pd.DataFrame: A DataFrame containing the timestamp, price, and volume data for the specified date range.

    Raises:
    - TypeError: If the coin is not a non-empty string or if the dates are not in the correct format.
    - ValueError: If the start date is not before the end date.
    - Exception: If the API request fails.
    """

    if not isinstance(coin, str) or not coin:
        raise TypeError("Coin must be a non-empty string.") 
    
    if isinstance(start_date, str):
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')

    if isinstance(end_date, str):
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
       
    if start_date >= end_date:
        raise ValueError("Start date must be before end date.") 
    
    coin = coin.lower() 

    url = f'https://api.coingecko.com/api/v3/coins/{coin}/market_chart/range'
    params = {
        'vs_currency': currency.lower(),
        'from': int(start_date.timestamp()),
        'to': int(end_date.timestamp())
    }
    
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
   
    volume = data['total_volumes']
    prices = data['prices']

    volume_values = [v[1] for v in volume] 
    
    assert len(prices) == len(volume_values), "Prices and volumes length mismatch!" 

    
    df = pd.DataFrame(prices, columns=['timestamp', 'price'],)

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['volume'] = volume_values
    
    return df