import joblib
from utils.preprocess import clean_text

# Load model once when the module is imported
model = joblib.load('model/sentiment_model.pkl')

def predict_sentiment(text_list):
    """
    Takes a list of raw reviews, cleans them, and returns predictions.
    """
    cleaned_reviews = [clean_text(r) for r in text_list]
    predictions = model.predict(cleaned_reviews)
    return predictions