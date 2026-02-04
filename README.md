# 🎬 IMDb Sentiment Pro

A full-stack NLP application that resolves movie titles via OMDb, scrapes real-time user reviews from IMDb, and classifies audience sentiment using a custom-trained Machine Learning model.

## 📊 The Pipeline
1. **Search Layer:** Resolves ambiguous titles (e.g., "Wanted") using OMDb API with poster previews.
2. **Data Acquisition:** Custom BeautifulSoup4 scraper to bypass IMDb's bot protection.
3. **NLP Engine:** Scikit-Learn Pipeline (TF-IDF Vectorizer + Logistic Regression).
4. **UI:** Streamlit dashboard with Glassmorphism UI and Plotly visualizations.



## 🛠️ Installation & Setup
1. Clone the repo: `git clone https://github.com/your-username/imdb-sentiment-analyzer.git`
2. Create Venv: `python -m venv venv`
3. Install Deps: `pip install -r requirements.txt`
4. Add API Key: Create a `.env` file and add `OMDB_API_KEY=your_key`
5. Train Model: `python -m model.train`
6. Run App: `streamlit run app.py`

## 📈 Model Performance
Trained on the **IMDb 50k Dataset**, capturing unigrams and bigrams for nuanced sentiment (e.g., understanding "not good").