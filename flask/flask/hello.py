from flask import Flask, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__)
#app.config.from_pyfile('config.py')
app.config['MONGO_URI'] = 'mongodb://user:pass@ds044709.mlab.com:44709/speakout'
mongo = PyMongo(app)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    # get db connection, use model
    if request.method == 'POST':
        print(request.form.get('email'), request.form.get('password'))
    return render_template('login.html')

@app.route("/profile/<username>")
def profile(username):
	return render_template('profile.html')

@app.route("/register")
def register():
    SEED_DATA = [
        {
            'decade': '1970s',
            'artist': 'Debby Boone',
            'song': 'You Light Up My Life',
            'weeksAtOne': 10
        },
        {
            'decade': '1980s',
            'artist': 'Olivia Newton-John',
            'song': 'Physical',
            'weeksAtOne': 10
        },
        {
            'decade': '1990s',
            'artist': 'Mariah Carey',
            'song': 'One Sweet Day',
            'weeksAtOne': 16
        }
    ]
#    mongo.db['songs'].insert_many(SEED_DATA);
    return render_template('signup.html')

if __name__ == "__main__":
	app.run(debug=True)
