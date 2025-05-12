import os
import requests

def search_web(entity, prompt):
    api_key = os.getenv("SERPAPI_KEY")
    query = prompt.replace("{company}", entity)
    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google"
    }
    response = requests.get("https://serpapi.com/search", params=params)
    return response.json().get("organic_results", [])