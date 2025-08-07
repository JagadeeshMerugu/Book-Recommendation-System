import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'books')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/book_recommendation_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

print("Succssfully configered")