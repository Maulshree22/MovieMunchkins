from flask import Flask
from models import MovieRating, MovieReview
from flask import Flask, render_template, request, redirect, url_for, session
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'YES'
app.config['MYSQL_DB'] = 'geeklogin'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)




# rating_handler = MovieRating()
# Example usage in routes.py
movie_id = 123  # Replace with actual movie ID
rating_value = 4.5  # Replace with the actual rating value
rating_handler = MovieRating(movie_id, rating_value)
# Example usage in app.py
movie_id = 123  # Replace with actual movie ID
review_text = "This movie was great!"  # Replace with the actual review text
review_handler = MovieReview(movie_id, review_text)


# review_handler = MovieReview()

# 
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

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')



if __name__ == '__main__': 
	app.debug=True
	app.run()