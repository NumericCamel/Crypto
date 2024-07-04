import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import string
import spacy

# Ensure nltk resources are downloaded
nltk.download('stopwords', quiet=True)
nltk.download('vader_lexicon', quiet=True)

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Initialize stopwords and SentimentIntensityAnalyzer
stop_words = set(stopwords.words('english'))
sia = SentimentIntensityAnalyzer()

# Blacklist of words
blacklist = set(['https', 'com', 'nan', 'www', 'amp', 'png', 'http', 'would', 'like', 'iâ', '000', 'io'])

def preprocess_text(text):
    if not isinstance(text, str):
        return ''
    # Convert text to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize text using spaCy's nlp pipeline
    tokens = nlp(text)
    
    # Remove stop words and non-alphabetic tokens, and perform lemmatization
    tokens = [token.lemma_ for token in tokens if token.is_alpha and token.text not in stop_words and token.text not in blacklist]
    
    # Join tokens back into a single string
    preprocessed_text = ' '.join(tokens)
    
    return preprocessed_text

def apply_sentiment_analysis(text):
    if pd.isna(text):
        # Return a neutral sentiment score for NaN entries
        return {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}
    return sia.polarity_scores(text)

def process_dataframe(df):
    # Preprocess title and selftext
    df['processed_title'] = df['title'].apply(preprocess_text)
    df['processed_text'] = df['selftext'].apply(preprocess_text)
    
    # Combine processed title and text
    df['combined_text'] = df['processed_title'] + ' ' + df['processed_text']
    
    # Apply sentiment analysis
    df['sentiment'] = df['combined_text'].apply(apply_sentiment_analysis)
    
    # Extract compound sentiment score
    df['sentiment_score'] = df['sentiment'].apply(lambda x: x['compound'])
    
    return df

def main(df):
    # Ensure required columns exist
    required_columns = ['title', 'selftext', 'date_posted']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"DataFrame must contain columns: {', '.join(required_columns)}")
    
    # Convert dates
    df['date_posted'] = pd.to_datetime(df['date_posted'], errors='coerce')
    
    # Process the dataframe
    processed_df = process_dataframe(df)
    
    # Select and return relevant columns
    return processed_df[['date_posted', 'sentiment_score']]

if __name__ == "__main__":
    # Example usage
    # df = pd.read_csv('your_data.csv')
    # result = main(df)
    # print(result)
    pass