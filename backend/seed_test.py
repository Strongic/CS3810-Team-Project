# Generated from gemini
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    # 1. Ask for a specific person
    target_name = "Landon"
    user = User.query.filter_by(username=target_name).first()

    if user:
        print(f"\nBooks in {user.username}'s collection:")
        # 2. Access the 'collection' relationship directly
        for book in user.collection:
            print(f" - {book.title} by {book.authors}")
    else:
        print("User not found!")