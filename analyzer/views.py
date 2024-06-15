from django.shortcuts import render
import pandas as pd
import dill as pickle
from textblob import TextBlob
from wordcloud import WordCloud
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import base64
from io import BytesIO

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

def generate_word_cloud(text):
    cloud = WordCloud(max_words=50, stopwords=set(stopwords.words("english"))).generate(str(text))
    plt.figure(figsize=(10, 10))
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis('off')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def home(request):
    df = pd.read_csv('analyzer/pre_analyzed_data.csv')
    return render(request, 'home.html', {'df': df.to_html(classes='table table-striped')})

def analyze_text(request):
    if request.method == 'POST':
        text = request.POST['text']
        sentiment = get_sentiment(text)
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
