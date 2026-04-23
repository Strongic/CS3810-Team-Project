import os
import sqlite3
import requests
from dotenv import load_dotenv

#load environment variables for api key
load_dotenv()
API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')

def init_db():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL
    )''')


    

def search_books(query):
    url = f"https://www.googleapis.com/books/v1/volumes"
    params = {
        'q': query,
        'key': API_KEY,
        'maxResults': 5
    }
    
    response = requests.get(url, params = params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.statuse_code}")
        return None



if __name__ == "__main__":
    if API_KEY:
        books = search_books("python programing")
        if books:
            for book in books.get('items', []):
                volume_info = book.get('volumeInfo', {})
                print(f"Title: {volume_info.get('title')}")
                print(f"Authors: {volume_info.get('authors', ['Unknown'])}")
                print("-"*20)
        else:
            print("API key not found in .env file")