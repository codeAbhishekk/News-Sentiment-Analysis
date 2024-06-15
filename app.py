# app.py

import streamlit as st
from textblob import TextBlob
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import base64
from io import BytesIO
import requests
from bs4 import BeautifulSoup
import dill as pickle

# Function to load sentiment analysis model
def load_sentiment_model():
    try:
        with open('analyzer/sentiment_model.pkl', 'rb') as file:
            pickled_objects = pickle.load(file)
            get_sentiment = pickled_objects['get_sentiment']
        return get_sentiment
    except FileNotFoundError:
        raise FileNotFoundError("sentiment_model.pkl not found. Make sure it exists and is accessible.")
    except (pickle.UnpicklingError, KeyError) as e:
        raise RuntimeError("Error loading sentiment_model.pkl: {}".format(e))

get_sentiment = load_sentiment_model()

# Function to generate word cloud
def generate_word_cloud(text):
    cloud = WordCloud(max_words=50, stopwords=set(stopwords.words("english"))).generate(str(text))
    plt.figure(figsize=(10, 10))
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis('off')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

# Function to scrape and analyze news
def scrape_and_analyze_news():
    url = 'https://www.ndtv.com/latest/page-8'
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    items = soup.find_all('div', class_='news_Itm')
    data = []

    for index, item in enumerate(items):
        if (index + 1) in [4, 8]:
            continue
        headline_tag = item.find('h2', class_='newsHdng')
        content_tag = item.find('p', class_='newsCont')
        if headline_tag and content_tag:
            headline = headline_tag.text.strip()
            content = content_tag.text.strip()
            sentiment = get_sentiment(content)
            sentiment_label = 'positive' if sentiment > 0 else 'negative' if sentiment < 0 else 'neutral'
            data.append({'index': index + 1, 'headline': headline, 'content': content, 'sentiment': sentiment, 'sentiment_label': sentiment_label})

    return pd.DataFrame(data)

# Main Streamlit application
def main():
    st.title('Sentiment Analysis Dashboard')
    st.write('Welcome to the Sentiment Analysis Dashboard.')

    # Display scraped and analyzed news in a table
    df = scrape_and_analyze_news()
    st.write(df)

    # Generate and display word cloud
    st.subheader('Word Cloud')
    image_base64 = generate_word_cloud(df['content'])
    st.image(image_base64, caption='Word Cloud', use_column_width=True)

if __name__ == '__main__':
    main()
