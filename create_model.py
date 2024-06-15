from textblob import TextBlob  # Ensure TextBlob is imported**

import dill as pickle
import os

def get_sentiment(text):
  """
  This function takes a text string and returns its sentiment polarity using TextBlob.

  Args:
      text: The text string to analyze.

  Returns:
      A float value between -1 (negative) and 1 (positive) representing the sentiment polarity.
  """
  blob = TextBlob(text)  # Use TextBlob from textblob module
  return blob.sentiment.polarity

# Dictionary containing the function you want to serialize
pickl = {
  'get_sentiment': get_sentiment,
}

# Ensure the analyzer directory exists
if not os.path.exists('analyzer'):
  os.makedirs('analyzer')

# Serialize the dictionary and save it to a file
with open('analyzer/sentiment_model.pkl', 'wb') as file:
  pickle.dump(pickl, file)

print("Model serialized successfully!")