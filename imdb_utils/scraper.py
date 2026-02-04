import requests
from bs4 import BeautifulSoup

def scrape_reviews(imdb_id):
    # We target the 'reviews' subpage directly
    url = f"https://www.imdb.com/title/{imdb_id}/reviews"
    
    print(f"📥 Attempting to scrape: {url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Failed to connect. Status Code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        
        # Method 1: The standard modern class
        review_containers = soup.find_all("div", class_="text show-more__control")
        
        # Method 2: Fallback to the general content div if Method 1 is empty
        if not review_containers:
            print("⚠️ Method 1 failed, trying Method 2...")
            review_containers = soup.select(".ipc-html-content-inner-div") 

        # Method 3: The legacy 'lister' class
        if not review_containers:
            print("⚠️ Method 2 failed, trying Method 3...")
            review_containers = soup.find_all("div", class_="content")

        reviews = [r.get_text(strip=True) for r in review_containers if len(r.get_text()) > 10]
        
        if reviews:
            print(f"✅ Success! Found {len(reviews)} reviews.")
            return reviews
        else:
            print("❌ No reviews found. IMDb might be blocking us or the ID is wrong.")
            # Save for debugging
            with open("scraper_debug.html", "wb") as f:
                f.write(response.content)
            return []

    except Exception as e:
        print(f"❌ Scraper error: {e}")
        return []

if __name__ == "__main__":
    # Test with Interstellar ID
    scrape_reviews("tt0816692")