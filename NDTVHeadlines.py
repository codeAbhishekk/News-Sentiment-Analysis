from django.shortcuts import render
import pandas as pd
import dill as pickle
from textblob import TextBlob
from wordcloud import WordCloud
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import requests
from bs4 import BeautifulSoup

# Function to load the sentiment model
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

# Function to generate a word cloud
def generate_word_cloud(text):
    cloud = WordCloud(max_words=50, stopwords=set(stopwords.words("english"))).generate(str(text))
    plt.figure(figsize=(10, 10))
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis('off')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

# Function to scrape NDTV news and analyze sentiment
def scrape_and_analyze_news():
    # URL of NDTV's latest news page
    url = 'https://www.ndtv.com/latest/page-8'
    
    # Send a GET request to fetch the HTML content
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    
    # Find all news item containers
    items = soup.find_all('div', class_='news_Itm')
    
    data = []
    
    # Iterate through the news items and extract headlines and content
    for index, item in enumerate(items):
        # Skip every 4th and 8th item
        if (index + 1) in [4, 8]:
            continue
        
        # Extract headlines and content
        headline_tag = item.find('h2', class_='newsHdng')
        content_tag = item.find('p', class_='newsCont')
        
        # Check if tags are not None before accessing text
        if headline_tag and content_tag:
            headline = headline_tag.text.strip()
            content = content_tag.text.strip()
            sentiment = get_sentiment(content)
            sentiment_label = 'positive' if sentiment > 0 else 'negative' if sentiment < 0 else 'neutral'
            
            data.append({'index': index + 1, 'headline': headline, 'content': content, 'sentiment': sentiment, 'sentiment_label': sentiment_label})
    
    return pd.DataFrame(data)

# Home view
def home(request):
    df = scrape_and_analyze_news()
    return render(request, 'home.html', {'df': df.to_html(classes='table table-striped')})

# Analyze text view
def analyze_text(request):
    if request.method == 'POST':
        text = request.POST['text']
        sentiment = get_sentiment(text)
        sentiment_label = 'positive' if sentiment > 0 else 'negative' if sentiment < 0 else 'neutral'


   