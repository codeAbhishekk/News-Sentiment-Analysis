from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pandas as pd
import dill as pickle
from textblob import TextBlob
from wordcloud import WordCloud
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import base64
from io import BytesIO



def get_sentiment(text):
    blob=TextBlob(text)
    return blob.sentiment.polarity



def generate_word_cloud(text):
    cloud = WordCloud(max_words=50, stopwords=set(stopwords.words("english"))).generate(str(text))
    plt.figure(figsize=(10, 10))
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis('off')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    return base64.b64encode(buffer.getvalue()).decode('utf-8')



def scrape_and_analyze_news():
    base_url = 'https://www.ndtv.com/latest/page-'
    pages = range(1, 9)  # Pages 1 to 8
    
    data = []
    
    for page_num in pages:
        url = base_url + str(page_num)
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')
        items = soup.find_all('div', class_='news_Itm')
        
        for index, item in enumerate(items):
            # Skip every 4th and 8th item, as these contain add.
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

# Home view
def home(request):
    df = scrape_and_analyze_news()
    return render(request, 'home.html', {'df': df.to_html(classes='table table-striped')})

def analyze_text(request):
    if request.method == 'POST':
        text = request.POST['text']
        blob = TextBlob(text)
        sentiment =blob.sentiment.polarity # get_sentiment(text)
        sentiment_label = 'positive' if sentiment > 0 else 'negative' if sentiment < 0 else 'neutral'
        return render(request, 'result.html', {'sentiment_label': sentiment_label, 'text': text})
    return render(request, 'analyze_text.html')

def analyze_csv(request):
    if request.method == 'POST' and request.FILES['file']:
        csv_file = request.FILES['file']
        df = pd.read_csv(csv_file)
        df['text'] = df['Headline'] + " " + df['Content']
        df['sentiment'] = df['text'].apply(get_sentiment)
        df['sentiment_label'] = df['sentiment'].apply(lambda x: 'positive' if x > 0 else 'negative' if x < 0 else 'neutral')

        image_base64 = generate_word_cloud(df['Content'])

        df.to_csv('analyzer/static/sentiment_analysis_results.csv', index=False)

        return render(request, 'result_csv.html', {'image_base64': image_base64, 'df': df.to_html(classes='table table-striped')})
    return render(request, 'analyze_csv.html')