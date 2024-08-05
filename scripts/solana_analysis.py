import pandas as pd
from run_reddit_sentiment import main as run_reddit_sentiment
# INPUT
    # 1. Reddit Sentiment Analysis
    # 2. Bitcoin, Ethereum, and Solana Prices 
    # 3. Wikipedia and Google Trends data 

# OUTPUT

reddit_data = pd.read_csv('reddit_pull/all_data.csv')
reddit_data = run_reddit_sentiment(reddit_data)