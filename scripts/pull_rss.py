import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to get the text of an article
def get_article_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        article_text = ' '.join([para.get_text() for para in paragraphs])
        return article_text
    except Exception as e:
        print(f"Failed to get article text: {e}")
        return ""

# Function to parse RSS feed and extract data
def parse_rss_feed(feed_url):
    feed = feedparser.parse(feed_url)
    articles = []

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        article_text = entry.description
        articles.append({
            'title': title,
            'link': link,
            'text': article_text
        })

    return articles

# Example usage
rss_feed_url = 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'  # Replace with the actual RSS feed URL
articles = parse_rss_feed(rss_feed_url)

# Create a DataFrame
df = pd.DataFrame(articles)

print(df.head())

