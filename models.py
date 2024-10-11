# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class MovieRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer)
    rating = db.Column(db.Integer)

    def __init__(self, movie_id, rating):
        self.movie_id = movie_id
        self.rating = rating

class MovieReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer)
    review = db.Column(db.String(500))

    def __init__(self, movie_id, review):
        self.movie_id = movie_id
        self.review = review

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float)
    reviews = db.relationship('Review', backref='movie', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float)
    text = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

