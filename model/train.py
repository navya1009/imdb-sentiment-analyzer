import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from utils.preprocess import clean_text

def train_model():
    print("📂 Loading 50,000 IMDb reviews...")
    try:
        df = pd.read_csv('data/IMDB Dataset.csv')
        
        # Convert text labels to numbers
        df['sentiment'] = df['sentiment'].map({'positive': 1, 'negative': 0})

        print("🧹 Cleaning data (this may take 2-3 minutes)...")
        df['review'] = df['review'].apply(clean_text)

        # TF-IDF Upgrade: 
        # ngram_range=(1,2) captures "not good" as a feature
        # max_features=10000 keeps the model size efficient
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=10000, ngram_range=(1, 2))),
            ('clf', LogisticRegression(max_iter=1000))
        ])

        print("🚀 Training production model...")
        pipeline.fit(df['review'], df['sentiment'])

        joblib.dump(pipeline, 'model/sentiment_model.pkl')
        print("✅ Success! Model updated. Ready for Interstellar.")
        
    except FileNotFoundError:
        print("❌ Error: 'data/IMDB Dataset.csv' not found.")

if __name__ == "__main__":
    train_model()