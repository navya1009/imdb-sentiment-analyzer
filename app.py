import streamlit as st
import joblib
import pandas as pd
import plotly.express as px
from imdb_utils.search import search_imdb_list
from imdb_utils.scraper import scrape_reviews
from utils.preprocess import clean_text

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="IMDb Sentiment Pro",
    page_icon="🎬",
    layout="wide"
)

# --- MODEL LOADING ---
@st.cache_resource 
def load_model():
    return joblib.load('model/sentiment_model.pkl')

try:
    model = load_model()
except Exception:
    st.error("Model file not found. Please run 'python -m model.train' first.")
    st.stop()

# --- HEADER ---
st.title("🎬 IMDb Sentiment Analyzer")
st.markdown("Find a movie, see the poster, and analyze real-time audience reception.")
st.divider()

# --- STEP 1: SEARCH ---
st.subheader("🔍 Step 1: Find your Movie or Series")
movie_query = st.text_input("Enter title (e.g., 'Interstellar') and press Enter:", placeholder="Search...")

if movie_query:
    results = search_imdb_list(movie_query)
    
    if results:
        with st.container(border=True):
            st.write(f"Found {len(results)} matches. Please refine your selection:")
            
            options = [f"{m['Title']} ({m['Year']}) - {m['Type'].capitalize()}" for m in results]
            selected_option = st.selectbox("Select the exact version:", options)
            
            selected_index = options.index(selected_option)
            movie_data = results[selected_index]
            selected_id = movie_data['imdbID']
            poster_url = movie_data['Poster']

            col_post, col_det = st.columns([1, 3])
            with col_post:
                if poster_url != "N/A":
                    st.image(poster_url, use_container_width=True)
                else:
                    st.info("No Poster Available")
            
            with col_det:
                st.write(f"### {selected_option}")
                st.write(f"**IMDb ID:** `{selected_id}`")
                st.write(f"**Category:** {movie_data['Type'].capitalize()}")
                analyze_btn = st.button("🚀 Run Sentiment Analysis", use_container_width=True, type="primary")

        # --- STEP 2: ANALYSIS ---
        if analyze_btn:
            st.divider()
            with st.spinner(f"📥 Analyzing reviews for {selected_option}..."):
                reviews = scrape_reviews(selected_id)
            
            if reviews:
                cleaned = [clean_text(r) for r in reviews]
                predictions = model.predict(cleaned)
                
                pos_count = int(sum(predictions))
                neg_count = len(predictions) - pos_count
                total = len(predictions)
                pos_percent = (pos_count / total) * 100

                # --- FANCY VERDICT (GLASSMORPHISM) ---
                color = "#2ecc71" if pos_percent >= 65 else "#e74c3c" if pos_percent <= 35 else "#f1c40f"
                st.markdown(f"""
                    <div style="background-color:{color}22; border-left: 10px solid {color}; padding: 25px; border-radius: 15px; margin-bottom: 30px; backdrop-filter: blur(10px);">
                        <h1 style="color:{color}; margin:0; font-size: 2.5rem;">{pos_percent:.1f}% Positive</h1>
                        <p style="color:white; margin:0; font-weight:bold; font-size: 1.2rem;">Verdict: {"Mostly Positive 😊" if pos_percent >= 65 else "Mostly Negative 😡" if pos_percent <= 35 else "Mixed Reviews 😐"}</p>
                        <p style="color:gray; margin:0;">Analyzed {total} real-time audience reviews.</p>
                    </div>
                """, unsafe_allow_html=True)

                col_m, col_c = st.columns([1, 1.2])
                
                with col_m:
                    st.write("#### Sentiment Breakdown")
                    st.metric("Total Reviews", total)
                    st.metric("Positive 👍", pos_count)
                    st.metric("Negative 👎", neg_count)

                # --- FANCY DONUT CHART ---
                with col_c:
                    chart_df = pd.DataFrame({
                        "Sentiment": ["Positive", "Negative"],
                        "Count": [pos_count, neg_count]
                    })
                    
                    fig = px.pie(
                        chart_df, values='Count', names='Sentiment',
                        color='Sentiment',
                        color_discrete_map={'Positive': '#2ecc71', 'Negative': '#e74c3c'},
                        hole=0.6
                    )
                    
                    # Update for fancy 3D/Pull effect
                    fig.update_traces(
                        textinfo='percent+label',
                        pull=[0.1, 0], # "Pull" the positive slice
                        marker=dict(line=dict(color='#FFFFFF', width=2)),
                        hoverinfo='label+value+percent',
                        textfont_size=14
                    )
                    
                    fig.update_layout(
                        showlegend=False,
                        annotations=[dict(text='RECEPTION', x=0.5, y=0.5, font_size=18, showarrow=False, font_color="gray")],
                        margin=dict(t=10, b=10, l=10, r=10),
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True, key=f"fancy_chart_{selected_id}")

                with st.expander("📖 View Sample Reviews"):
                    for i, r in enumerate(reviews[:10]):
                        icon = "🟢" if predictions[i] == 1 else "🔴"
                        st.markdown(f"{icon} **Review {i+1}**")
                        st.write(f"_{r[:500]}_...")
                        st.markdown("---")
            else:
                st.error("No reviews found for this title.")
    else:
        st.error("No matches found. Try a different title.")

st.markdown("---")
st.caption("Custom Project using OMDb API and Scikit-Learn Logistic Regression.")