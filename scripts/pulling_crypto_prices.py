from datetime import datetime
import pandas as pd
import requests
import time


def construct_url(ticker, period_1, period_2, interval='daily'):
    """
    Parameters
    ----------
    ticker : str
        ticker symbol
    period_1 : str
        start date in 'YYYY-MM-DD' format
    period_2 : str
        end date in 'YYYY-MM-DD' format
    interval : str
        time interval, one of 'daily', 'weekly', 'monthly'
    """
    def convert_to_seconds(period):
        datetime_value = datetime.strptime(period, '%Y-%m-%d')
        total_seconds = int(time.mktime(datetime_value.timetuple()))
        return total_seconds

    try:
        interval_dic = {'daily': '1d', 'weekly': '1wk', 'monthly': '1mo'}
        _interval = interval_dic.get(interval)
        if _interval is None:  
            print('interval code is incorrect')
            return None
        p1 = convert_to_seconds(period_1)
        p2 = convert_to_seconds(period_2)
        url = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={p1}&period2={p2}&interval={_interval}&events=history'
        return url
    
    except Exception as e:
        print(e)
        return None

query_url = construct_url('BTC-USD', '2020-01-01', '2024-07-08')
if query_url:
    try:
        response = requests.get(query_url)
        response.raise_for_status()  # Check if the request was successful
        btc = pd.read_csv(pd.compat.StringIO(response.text))
        print(btc.head())
    except requests.exceptions.RequestException as e:
        print(f"HTTP request error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
else:
    print("Failed to construct URL.")
    
#query_url = construct_url('BTC-USD', '2020-01-01', '2024-01-01')
#btc = pd.read_csv(query_ur


# Function to download the file with retries
def download_file(url, retries=5, backoff_factor=0.3):
    for i in range(retries):
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            with open('downloaded_file.csv', 'wb') as file:
                file.write(response.content)
            print("Download successful")
            return
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:  # Too many requests
                wait = backoff_factor * (2 ** i)
                print(f"Too many requests. Retrying in {wait} seconds...")
                time.sleep(wait)
            else:
                raise e
    raise Exception("Failed to download file after several retries")

# Download the file
download_file(query_url)

# Read the CSV file into a pandas DataFrame (optional)
df = pd.read_csv('downloaded_file.csv')

# Display the DataFrame (optional)
print(df)





