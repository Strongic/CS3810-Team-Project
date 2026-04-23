# populate user database and book database with dummy data
# Generated with Gemini

import os
from app import create_app, db
from app.models import User, Book
from app.services import fetch_books_from_api
import random

def seed_database():
    app = create_app()
    with app.app_context():
        print("Cleaning database...")
        db.drop_all()
        db.create_all()

        # 1. Create a Variety of Users
        print("Creating dummy users...")
        users_to_create = [
            {"username": "Landon", "has_books": True},
            {"username": "Steve_Prof", "has_books": True},
            {"username": "Newbie_User", "has_books": False},  # Empty collection
            {"username": "Guest_Account", "has_books": False}, # Empty collection
            {"username": "Book_Worm_99", "has_books": True}
        ]
        
        user_objects = []
        for u_data in users_to_create:
            user = User(username=u_data["username"])
            db.session.add(user)
            user_objects.append((user, u_data["has_books"]))
        
        db.session.commit()

        # 2. Fetch Books from API
        print("Fetching books from Google API...")
        topics = ["software engineering", "colorado history", "science fiction"]
        all_fetched_books = []

        for topic in topics:
            books_data = fetch_books_from_api(topic)
            for item in books_data:
                v_info = item.get('volumeInfo', {})
                # Ensure we don't add duplicates
                if not Book.query.filter_by(google_id=item['id']).first():
                    new_book = Book(
                        google_id=item['id'],
                        title=v_info.get('title', 'Unknown Title'),
                        authors=", ".join(v_info.get('authors', ['Unknown Author']))
                    )
                    db.session.add(new_book)
                    all_fetched_books.append(new_book)
        
        db.session.commit()

        # 3. Dynamic Relationship Assignment
        print("Populating user collections...")
        for user, should_have_books in user_objects:
            if should_have_books:
                # Assign between 3 to 8 random books from our pool
                num_books = random.randint(3, 8)
                selected_books = random.sample(all_fetched_books, num_books)
                
                for b in selected_books:
                    user.collection.append(b)
                
                print(f" - Added {num_books} books to {user.username}'s collection.")
            else:
                print(f" - Leaving {user.username}'s collection empty (New User).")

        db.session.commit()
        print("\nDatabase Seeding Complete!")

if __name__ == "__main__":
    seed_database()