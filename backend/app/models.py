from . import db

# junction table for many-to-many relationship
user_books = db.Table('user_books',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.book_id'), primary_key=True)
)

# mapping class to database named 'User'. 
# primary key ensured each ID tag is unique/different.
# unique ensures no 2 rows have the same value for its column. 
# nullable=false ensures everyone has a username in the table.
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Stirng(80), unique=True, nullable=False)
    
    #create link between users and books through junction table
    collection = db.relationship('Book', secondary=user_books, backref='owners')

#mapping class to database named 'Book'.
class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column()
    title = db.Column()
    author = db.Column()