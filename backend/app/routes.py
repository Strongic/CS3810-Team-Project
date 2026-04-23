# Combine services.py and models.py. Check database and adds the connection
from flask import Blueprint, request, jsonify
from .models import db, User, Book
from .services import fetch_books_from_api

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return {"message": "Library System API is Up and Running!"}

@main.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')

    results = fetch_books_from_api(query)
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