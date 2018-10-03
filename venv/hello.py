from flask import Flask, render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo
from flask_socketio import SocketIO

app = Flask(__name__)
#app.config.from_pyfile('config.py')
app.config["MONGO_URI"] = 'mongodb://test123:test123@ds030817.mlab.com:30817/testpls123'

mongo = PyMongo(app)
socketio = SocketIO(app)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    # get db connection, use model
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = mongo.db.users.find_one({'email': email})
        if user is not None and password == user.get('password'):
            session['logged_in'] = True
            session['user_email'] = email
            return redirect(url_for('profile'))
        else:
            error = 'invalid username or password'
    
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in')
    session.pop('user_email')
    
    return redirect(url_for('login'))

@app.route("/profile")
@app.route("/profile/<email>")
def profile(email=None):
    if email is None:
        email = session['user_email']
    user = mongo.db.users.find_one({'email': email})
    posts = [x for x in mongo.db.posts.find({'email': email})]
    return render_template('profile.html', user=user, posts=posts)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_info = {
            'email': request.form.get('email'),
            'name': request.form.get('name'),
            'password': request.form.get('password'),
            'gender': request.form.get('gender'),
            'industry': request.form.get('industry'),
            'race': request.form.get('race')
        }
        mongo.db.users.insert_one(user_info)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route("/map")
def map():
    coords = []
    for x in mongo.db.coords.find():
        coords.append({'lat': x['lat'], 'lng': x['lng']})
    return render_template('maps.html', coords=coords)

@app.route("/stats")
def stats():
    posts = [x for x in mongo.db.posts.find()]
    return render_template('stats.html', posts=posts)

@app.route("/post", methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        post_info = {
            'topic': request.form.get('topic'),
            'type': request.form.get('type'),
            'message': request.form.get('message'),
            'email': session['user_email']
        }
        mongo.db.posts.insert_one(post_info)
        return redirect(url_for('profile'))
    return render_template('post.html')

@app.route("/newsfeed")
def newsfeed():
    posts = [x for x in mongo.db.posts.find()]
    return render_template('newsfeed.html', posts = posts)

@socketio.on('my event')
def handle_my_custom_event(json):
    print(json)
    mongo.db.coords.insert_one(json);

if __name__ == "__main__":
    socketio.run(app)
	#app.run()
