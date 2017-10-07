from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login")
def login():
	return render_template('login.html')

@app.route("/profile/<username>")
def profile(username):
	return render_template('profile.html')

@app.route("/register")
def register():
	return render_template('signup.html')

if __name__ == "__main__":
	app.run(debug=True)