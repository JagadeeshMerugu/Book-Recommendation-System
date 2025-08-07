# models.py

# NOT USED
from app import db

class User(db.Model):
    __tablename__ = 'users'
    User_ID = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email_id = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    Location = db.Column(db.String(150))
    Age = db.Column(db.Integer)

class Book(db.Model):
    __tablename__ = 'books'
    ISBN = db.Column(db.String(20), primary_key=True)
    Book_Title = db.Column(db.String(200))
    Book_Author = db.Column(db.String(100))
    Year = db.Column(db.Integer)
    Publisher = db.Column(db.String(100))
    Genre = db.Column(db.String(100))
    Image_URL = db.Column(db.String(255))

class Rating(db.Model):
    __tablename__ = 'ratings'
    Rating_id = db.Column(db.Integer, primary_key=True)
    User_ID = db.Column(db.Integer, db.ForeignKey('users.User_ID'))
    ISBN = db.Column(db.String(20), db.ForeignKey('books.ISBN'))
    Rating = db.Column(db.Integer)




