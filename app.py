import requests
import os
from flask import (
    Flask,
    request,
    render_template,
    flash,
    url_for,
    session,
    redirect,
    jsonify,
    send_from_directory
)
import uuid
from werkzeug.utils import secure_filename
from functools import wraps
import bcrypt
import pymongo
#################################
##### I'M WORTHLESS GUY :') #####
#################################

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login")
            return render_template('guest.html')


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ERR_CODES = [400, 401, 403, 404, 500, 502, 503, 504]

db_link = "mongodb+srv://yigit:yigitinsifresi@projectdatabasegalbul.ixx82u7.mongodb.net/test"
client = pymongo.MongoClient(db_link)
db = client.galbul

app = Flask(__name__, instance_relative_config=True)
# default value during development
app.secret_key = 'yigitinsifresi'
# overridden if this file exists in the instance folder
app.config.from_pyfile('config.py', silent=True)
# Set up a MongoDB client and database

# Define the routes for registering, logging in, and logging out users
@app.route('/register', methods=['POST'])
def register():
    # Get the user's information from the request
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    parselNo = request.form['parselNo']
    bio = request.form["bio"]
    # Hash the password with bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Add the user to the database
    db.users.insert_one({
        'username': username,
        'password': hashed_password,
        'email': email,
        'parselNo': parselNo,
        "_id": str(uuid.uuid4()),
        "bio": bio
    })

    return render_template('register_index.html')

def get_session_user():
    if 'user_id' not in session:
        return None
    user_id = session['user_id']
    # fetch the user from database somehow
    user = db.users.find_one({
        '_id': user_id
    })
    return user

@login_required
@app.route('/profile/<string:user_id>', methods=["GET"])
def profile(user_id):
    user = get_user_from_id(user_id)
    return render_template('profile.html', user=user)

@app.route('/sikayet/<string:comp_user_id>', methods=["GET", "POST"])
def compliment(comp_user_id):
    user = get_session_user()
    return render_template('compliment.html', user=user, sikayet=get_user_from_id(comp_user_id))

def get_user_from_id(user_id):
    return db.users.find_one({
        "_id": user_id
    })
@app.route('/login', methods=['POST'])
def login():
    # Get the user's information from the request
    username = request.form['username']
    password = request.form['password']

    # Retrieve the user from the database
    user = db.users.find_one({'username': username})

    # Check that the user exists and the password is correct
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        # Add the user's id to the session
        session['user_id'] = str(user['_id'])
        return render_template('login_success.html')
    else:
        return render_template('login_error.html')

@app.route('/logout', methods=['GET'])
def logout():
    # Remove the user's id from the session
    session.pop('user_id', None)
    return render_template('logout.html')

@app.route('/kayit', methods = ["GET"])
def kayit():
    if request.method == "GET":
        return render_template('signup.html')

@app.route('/giris', methods=["GET"])
def giris():
    if request.method == "GET":
        return render_template('login.html')

def allowed_file(filename):
    return ('.' in filename) and (filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)

@app.route('/ziyaretci')
@app.route('/', methods = ["GET"])
def guest():
    return render_template('guest.html')

@app.route('/home')
@app.route('/home/', methods=['GET', 'POST'])
def index():
    user = get_session_user()
    if request.method == 'POST':
        dosya = request.files['dosya']
        dosya_adi = dosya.filename
        if allowed_file(dosya_adi):
            dosya.save('webimgs/'+dosya_adi)
        else:
            return render_template('upload_error.html')
    return render_template('index.html', user=user)

@app.route('/parselSorgu/<float:enlem>/<float:boylam>', methods=["GET"])
def parselSorgu(enlem, boylam):
    data = requests.get(f"https://cbsapi.tkgm.gov.tr/megsiswebapi.v3/api/parsel/{enlem}/{boylam}")
    response_json = data.json()
    req_json = {
        "enlem": str(enlem),
        "boylam": str(boylam),
        "parselObj": response_json
    }
    if data.status_code not in ERR_CODES:
        send_to_db(req_json)

        return jsonify(response_json)
    else:
        return jsonify({
            "error": "cannot get data",
            "status": str(data.status_code)
        })

def send_to_db(obj: dict) -> str:
    with pymongo.MongoClient(db_link) as client:
        collection_db = client["galbul"]
        db = collection_db.parsel

        response = db.insert_one(obj)
        if response == None:
            raise ValueError("Database cannot get accessable or not good. :D")

def get_db(link:str):
    with pymongo.MongoClient(db_link) as client:
        collection_db = client["galbul"]
        db = collection_db.parsel

        all_db = db.find({})
@app.route('/logo.png')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'logo.png',mimetype='image/png')
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=1)
    #or flask run --host=0.0.0.0 --port=8080
    #or python3 app.py --host=0.0.0.0 --port=8080
