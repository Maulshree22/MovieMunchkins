from flask import request, jsonify
from app import app
from models import MovieRating, MovieReview
from flask import request, jsonify
from models import db, Review

@app.route('/add_review', methods=['POST'])
def add_review():
    data = request.json
    movie_id = data.get('movie_id')
    rating = data.get('rating')
    review_text = data.get('review_text')

    if not all([movie_id, rating, review_text]):
        return jsonify({'error': 'Missing data.'}), 400

    review = Review(movie_id=movie_id, rating=rating, text=review_text)
    db.session.add(review)
    db.session.commit()

    return jsonify({'message': 'Review added successfully.'}), 201

# Example usage in routes.py
movie_id = 123  # Replace with actual movie ID
rating_value = 4.5  # Replace with the actual rating value
rating_handler = MovieRating(movie_id, rating_value)

# Example usage in app.py
movie_id = 123  # Replace with actual movie ID
review_text = "This movie was great!"  # Replace with the actual review text
review_handler = MovieReview(movie_id, review_text)


# rating_handler = MovieRating()
# review_handler = MovieReview()

@app.route('/api/movies/<int:movie_id>/ratings', methods=['POST'])
def add_rating(movie_id):
    rating = request.json.get('rating')
    if not rating:
        return jsonify({'error': 'Rating is required'}), 400
    rating_handler.add_rating(movie_id, rating)
    return jsonify({'message': 'Rating added successfully'}), 201

@app.route('/api/movies/<int:movie_id>/reviews', methods=['POST'])
def add_review(movie_id):
    review = request.json.get('review')
    if not review:
        return jsonify({'error': 'Review is required'}), 400
    review_handler.add_review(movie_id, review)
    return jsonify({'message': 'Review added successfully'}), 201
