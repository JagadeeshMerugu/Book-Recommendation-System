# train_models.py

import pandas as pd
import pickle
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sqlalchemy import create_engine

# --- DB connection ---
db_uri = "mysql+pymysql://root:root@localhost/book_recommendation_db"
engine = create_engine(db_uri)

# --- Load data ---
ratings_df = pd.read_sql("SELECT * FROM ratings", engine)
books_df = pd.read_sql("SELECT * FROM books", engine)

# --- Collaborative Filtering (KNN) ---
def train_knn_model():
    user_book_matrix = ratings_df.pivot(index='User_ID', columns='ISBN', values='Book_Rating').fillna(0)
    knn = NearestNeighbors(metric='cosine', algorithm='brute')
    knn.fit(user_book_matrix.values)
    with open("ml_models/knn_model.pkl", "wb") as f:
        pickle.dump((knn, user_book_matrix), f)
    print("✅ Saved: models/knn_model.pkl")

# --- Content-Based Filtering (TF-IDF) ---
def train_tfidf_model():
    books_df['features'] = books_df['Book_Title'] + ' ' + books_df['Book_Author'] + ' ' + books_df['Genre'].fillna('')
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(books_df['features'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    with open("ml_models/tfidf_vectorizer.pkl", "wb") as f:
        pickle.dump((tfidf, cosine_sim, books_df), f)
    print("✅ Saved: models/tfidf_vectorizer.pkl")

    

def train_all_models():
    train_knn_model()
    train_tfidf_model()
    print("📦 All models trained and saved.")

if __name__ == "__main__":
    train_knn_model()
    train_tfidf_model()
    print("📦 All models trained and saved.")
