# Combine services.py and models.py. Check database and adds the connection
from flask import Blueprint, request, jsonify
from .models import db, User, Book
from .services import fetch_books_from_api

main = Blueprint('main', __name__)

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()


    if user and user.password == data.get('password'):
        return jsonify({
            "user_id": user.user_id,
            "username": user.username
        }), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password') # no hashing yet

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered"}), 201

@main.route('/')
def home():
    return {"message": "Library System API is Up and Running!"}


"""This is for searching using the API directly"""
# @main.route('/search', methods=['GET'])
# def search():
#     query = request.args.get('q')

#     results = fetch_books_from_api(query)
#     return jsonify(results)


"""This is for searching using seed.py"""
@main.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    
    # This searches your local database for titles or authors that match the query
    books = Book.query.filter(
        (Book.title.ilike(f'%{query}%')) | 
        (Book.authors.ilike(f'%{query}%'))
    ).all()

    # Convert the SQLAlchemy objects into a list of dictionaries for the UI
    results = []
    for b in books:
        results.append({
            "book_id": b.book_id,
            "title": b.title,
            "authors": b.authors,
            "google_id": b.google_id,
            "genre": "General",  # Defaulting since we didn't seed genres
            "description": "A local library book." # Defaulting for now
        })
    
    return jsonify(results)


@main.route('/collection/add', methods=['POST'])
def add_to_collection():
    data = request.get_json()
    user_id = data.get('user_id')
    
    # We check for book_id (from our DB) or google_id (from the API)
    book_id = data.get('book_id')
    google_id = data.get('google_id')

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # 1. Find the book in our database
    if book_id:
        book = Book.query.get(book_id)
    else:
        book = Book.query.filter_by(google_id=google_id).first()

    # 2. If the book doesn't exist yet (e.g. from a fresh API search), create it
    if not book:
        book = Book(
            google_id=google_id,
            title=data.get('title'),
            authors=data.get('authors')
        )
        db.session.add(book)
        db.session.flush() # Gets the ID without committing yet

    # 3. Link to user if not already there
    if book not in user.collection:
        user.collection.append(book)
        db.session.commit()
        return jsonify({"message": "Book added to your collection!"}), 200
    
    return jsonify({"message": "Book is already in your collection."}), 200


@main.route('/collection/remove', methods=['POST'])
def remove_from_collection():
    data = request.get_json()
    user_id = data.get('user_id')
    book_id = data.get('book_id')

    user = User.query.get(user_id)
    book = Book.query.get(book_id)

    if not user or not book:
        return jsonify({"error": "User or Book not found"}), 404
    
    if book in user.collection:
        user.collection.remove(book)
        db.session.commit()
        return jsonify({"message": "Book returned successfully!"}), 200
    return jsonify({"error": "This book is not in your collection."}), 400