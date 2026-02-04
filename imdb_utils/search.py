import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY", "").strip()
BASE_URL = "http://www.omdbapi.com/"

def search_imdb_list(movie_name):
    if not API_KEY or len(movie_name) < 3: # Don't search for 1-2 letters to save API calls
        return []

    params = {"apikey": API_KEY, "s": movie_name.strip()}
    
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        if data.get("Response") == "True":
            # This returns Title, Year, imdbID, Type, and Poster
            return data.get("Search", [])
        return []
    except Exception as e:
        return []