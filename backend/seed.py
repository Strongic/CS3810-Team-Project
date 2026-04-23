import os
from app import create_app, db
from app.models import User, Book
from app.services import fetch_books_from_api

def seed_books_only():
    app = create_app()
    with app.app_context():
        print("Wiping database for a clean start...")
        db.drop_all()
        db.create_all()

        print("Fetching books from Google API...")
        # You can add as many topics as you want here
        topics = ["software engineering", "distributed systems", "python programming"]
        
        for topic in topics:
            books_data = fetch_books_from_api(topic)
            for item in books_data:
                v_info = item.get('volumeInfo', {})
                
                # Check for duplicates by google_id
                if not Book.query.filter_by(google_id=item['id']).first():
                    new_book = Book(
                        google_id=item['id'],
                        title=v_info.get('title', 'Unknown Title'),
                        authors=", ".join(v_info.get('authors', ['Unknown Author']))
                    )
                    db.session.add(new_book)
        
        db.session.commit()
        print(f"Success! Database now contains {Book.query.count()} books.")
        print("The User table is currently empty and ready for registrations.")

if __name__ == "__main__":
    seed_books_only()