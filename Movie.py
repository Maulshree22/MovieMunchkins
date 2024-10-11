# Importing required functions 
from flask import Flask, request, render_template 

# Flask constructor 
app = Flask(__name__) 

# Root endpoint 
@app.route('/', methods=['GET']) 
def index(): 
	## Display the HTML form template 
	return render_template('index.html') 

# `read-form` endpoint 
@app.route('/read-form', methods=['POST']) 
def read_form(): 

	# Get the form data as Python ImmutableDict datatype 
	data = request.form 

	## Return the extracted information 
	return {
		'name':data['username'],
		'emailId'	 : data['id'], 
		'password' : data['userPassword'],  
	} 

# Main Driver Function 
if __name__ == '__main__': 
	# Run the application on the local development server 
	app.run()
