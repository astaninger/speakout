from flask import Flask, render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_pyfile('config.py')
mongo = PyMongo(app)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    # get db connection, use model
    if request.method == 'POST':
        email = request.form.email
        password = request.form.password
        user = mongo.db.users.find_one({'email': email})
        print(user)
        if user is not None and user.password = password:
            session['logged_in'] = True
            session['user_email'] = email
            return redirect(url_for('profile', name=user.name))
        else:
            error = 'invalid username or password'
    
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in')
    session.pop('user_email')
    
    return redirect(url_for('login'))

@app.route("/profile/<name>")
def profile(name):
	return render_template('profile.html', name=name)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_info = {
            'email': request.form.email,
            'name': request.form.name,
            'password': request.form.password or None,
            'gender': request.form.gender or None,
            'industry': request.form.industry or None,
            'posts':[]
        }
        mongo.db.users.insert_one(user_info)
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route("/maps")
def maps():
    return render_template('maps.html')

@app.route("/stats")
def stats():
    return render_template('stats.html')

@app.route("/songs")
def songs():
    mongo.db.authenticate('user', 'pass')
    songs = [x for x in mongo.db.songs.find()]
    return render_template('songs.html', songs=songs)

if __name__ == "__main__":
	app.run(debug=True)
