# train_models.py

import pickle
import pandas as pd
from models import db, Rating, Book
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy.orm import joinedload

def train_all_models():
    # 1. Load ratings from DB
    ratings = Rating.query.all()
    rating_data = [(r.User_ID, r.ISBN, r.Book_Rating) for r in ratings]
    rating_df = pd.DataFrame(rating_data, columns=['User_ID', 'ISBN', 'Book_Rating'])

    if rating_df.empty:
        return

    # 2. Create pivot table for CF
    pivot = rating_df.pivot_table(index='User_ID', columns='ISBN', values='Book_Rating').fillna(0)
    with open('models/pivot.pkl', 'wb') as f:
        pickle.dump(pivot, f)

    # 3. KNN model (Collaborative Filtering)
    model = NearestNeighbors(metric='cosine', algorithm='brute')
    model.fit(pivot)
    with open('models/knn_model.pkl', 'wb') as f:
        pickle.dump(model, f)

    # 4. Content-based filtering (TF-IDF)
    books = Book.query.options(joinedload(Book)).all()
    books_data = [{
        "Book_Title": b.Book_Title,
        "Book_Author": b.Book_Author,
        "Genre": b.Genre,
        "ISBN": b.ISBN,
        "Image_URL_M": b.Image_URL_M
    } for b in books]

    books_df = pd.DataFrame(books_data)
    books_df['combined'] = books_df['Book_Title'] + " " + books_df['Book_Author'] + " " + books_df['Genre']

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(books_df['combined'])

    with open('models/tfidf.pkl', 'wb') as f:
        pickle.dump(tfidf, f)
    with open('models/tfidf_matrix.pkl', 'wb') as f:
        pickle.dump(tfidf_matrix, f)
    with open('models/books_df.pkl', 'wb') as f:
        pickle.dump(books_df, f)

    print("✅ Models trained and saved successfully.")

# Allow running directly from CLI too
if __name__ == '__main__':
    train_all_models()
