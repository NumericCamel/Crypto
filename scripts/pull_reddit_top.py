import pandas as pd
import requests
import pdb
from datetime import datetime, timezone
import os 
import os
path = 'C:/Users/mulle/Documents/iCloudDrive/Documents/19. GITHUB/Crypto'
os.chdir(path)

CLIENT_ID = 'xxxxx'
SECRET_KEY = 'xxxxxx'

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

data = {
# Removed Passcodes
}

headers = {'User-Agent': 'SolanaAPI/0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token',
                  auth=auth, data=data, headers=headers)

TOKEN = res.json()['access_token']

headers = {**headers, **{'Authorization': f'bearer {TOKEN}'}}

res_bitcoin = requests.get('https://oauth.reddit.com/r/bitcoin/hot?limit=100',
                  headers = headers)

res_solana = requests.get('https://oauth.reddit.com/r/solana/hot?limit=100',
                  headers = headers)

res_eth = requests.get('https://oauth.reddit.com/r/ethereum/hot?limit=100',
                  headers = headers)

crypto_red = requests.get('https://oauth.reddit.com/r/crypto/hot?limit=100',
                  headers = headers)

crypto_cur_red = requests.get('https://oauth.reddit.com/r/CryptoCurrency/hot?limit=100',
                  headers = headers)

fiance = requests.get('https://oauth.reddit.com/r/finance/hot?limit=100',
                  headers = headers)

def process_posts(json_data):
    # Initialize an empty list to store post data
    posts_data = []

    # Loop through each post in the JSON data
    for post in json_data['data']['children']:
        # Convert the Unix timestamp to a datetime object
        created_date = datetime.fromtimestamp(post['data']['created_utc']).strftime('%m/%d/%Y')

        # Get the current system date
        pull_date = datetime.now().strftime('%m/%d/%Y')

        # Append the data as a dictionary to the list
        posts_data.append({
            'subreddit': post['data']['subreddit'],
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'upvote_ratio': post['data']['upvote_ratio'],
            'ups': post['data']['ups'],
            'downs': post['data']['downs'],
            'score': post['data']['score'],
            'comments': post['data']['num_comments'],
            'date_posted': created_date,
            'pull_date': pull_date  # Add the pull_date to the data
        })

    # Convert the list of dictionaries to a DataFrame
    return pd.DataFrame(posts_data)

btc_reddit_new = process_posts(res_bitcoin.json())
eth_reddit_new = process_posts(res_eth.json())
sol_reddit_new = process_posts(res_solana.json())
crypto_reddit_new = process_posts(crypto_red.json())
crypto_cur_reddit_new = process_posts(crypto_cur_red.json())
fiance_reddit_new = process_posts(fiance.json())

all_data = pd.concat([btc_reddit_new, eth_reddit_new, sol_reddit_new, crypto_reddit_new, crypto_cur_reddit_new, fiance_reddit_new])
all_data.date_posted = pd.to_datetime(all_data.date_posted)
all_data['selftext'] = all_data['selftext'].fillna('')
all_data['text'] = all_data['title'] + ' ' + all_data['selftext']
all_data = all_data.drop_duplicates(subset=['text'], keep='first')

all_data.to_csv('data/raw/reddit_pull/all_data.csv', index=False)
print('Run Successful')
