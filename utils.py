import datetime
import requests

# Function to get the current date
def get_current_date():
    return datetime.datetime.now().strftime("%B %d, %Y")

# Function to perform Google Search using API
def google_search(query, api_key, cse_id):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cse_id,
        "num": 3  # Get top 3 results
    }
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        results = data.get("items", [])

        if not results:
            return "No relevant search results found.", []

        search_output = ""
        sources = []
        for item in results:
            search_output += f"🔹 **[{item['title']}]({item['link']})**\n\n{item['snippet']}\n\n"
            sources.append(f"[{item['title']}]({item['link']})")

        return search_output, sources

    except requests.exceptions.RequestException as e:
        return f"⚠️ Google Search API Error: {str(e)}", []
