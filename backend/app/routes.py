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

# @main.route('/search', methods=['GET'])
# def search():
#     query = request.args.get('q')

#     results = fetch_books_from_api(query)
#     return jsonify(results)

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


@main.route('/save-book', methods=['POST'])
def save_book():
    data = request.json

    #check if book already exists locally
    book = Book.query.filter_by(google_id=data['id']).first()
    if not book:
        book = Book(
            google_id = data['id'],
            title = data['volumeInfo']['title'],
            authors = ", ".join(data['volumeInfo'].get('authors', []))
        )
        db.session.add(book)
    
    # link to user
    user = User.query.get(data['user_id'])
    if book not in user.collection:
        user.collection.append(book)
        db.session.commit()

    return jsonify({"message": "Book added to collection!"})