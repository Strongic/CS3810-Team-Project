# Google Books API handler. Returns raw data
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')

def fetch_books_from_api(query):
    url = f"https://www.googleapis.com/books/v1/volumes"
    params = {
        'q': query,
        'key': API_KEY,
        'maxResults': 10
        }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json().get('items', [])
    return[]