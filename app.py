#!/bin/python3
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
import time
import uuid
from werkzeug.utils import secure_filename
from functools import wraps
import bcrypt
import pymongo
import urllib.parse
import threading
#for fatih internet
import certifi
#################################
##### I'M WORTHLESS GUY :') #####
#################################

project_name = "GalBul"
app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'yigitinsifresi'
app.config.from_pyfile('config.py', silent=True)
path = os.getcwd()

app.config["OPENSSL_CONF"] = path+'/openssl.cnf'
os.environ["OPENSSL_CONF"] = path+'/openssl.cnf'

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
cacert = certifi.where()
client = pymongo.MongoClient(db_link, tlsCAFile=cacert,tlsAllowInvalidCertificates=True)
db = client.galbul


@app.route('/banned', methods=["GET"])
def banned():
    flash('You are banned')
    time.sleep(2)
    return redirect('/register')


@app.route('/register', methods=['POST'])
def register():
    # Gönderilen isteğe bağlı kullanıcı parametrelerini eklemek.
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    adaNo = request.form['adaNo']
    parselNo = request.form['parselNo']
    ilTercihi = request.form['ilTercihi']
    
    # Şifreyi hashleyip veritabanına eklemek için
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Kullanıcı veritabanına ekleme kısmı
    is_user_exist = db.users.find_one({"email": email})
    is_user_banned = db.banned_emails.find_one({"email": email})
    not_exist_situtations = [None, False]
    if is_user_banned:
        return redirect('/banned')
    if (is_user_exist in not_exist_situtations):
        db.users.insert_one({
            ######################################################
            'username': username,                                #
            'password': hashed_password,                         #
            'email': email,                                      #
            'adaNo': adaNo,                                      #
            'parselNo': parselNo,                                #
            '_id': str(uuid.uuid4()),                            #
            'il': ilTercihi,                                     #
            'user_photos': []                                    #
            ######################################################
        })
        user = db.users.find_one({'email': email})
        session['user_id'] = str(user['_id'])
        return redirect('/home')
        
    else:
        return render_template('user_exist.html')

# @login_required
# @app.route('/arat', methods=['GET'])
# def search():
#     if 'user_id' not in session:
#         return redirect('/ziyaretci')

#     # Get the search query from the reques1t
#     query = request.args.get('query')

#     # Search the database for users matching the query
#     users = db.users.find({ 'name': { '$regex': query } })
    
#     # Render the search results in a Jinja template
#     return render_template('search_results.html', users=users, project_name=project_name)


@login_required
@app.route('/search', methods=["POST", "GET"])
def backend_of_search():
    if 'user_id' not in session:
        return redirect('/ziyaretci')
    session_user = get_session_user()
    
    query = request.form['query'].lower()
    username_query = urllib.parse.unquote(query).lower()  
    
    users = db.users.find({})
    wanted_users = []
    for userx in users:
        if userx['username'].lower() == username_query.lower():
            wanted_users.append(userx)
        else:
            pass
    
    if len(wanted_users) < 1:
        return render_template('search_not_found.html')
    return render_template('search_results.html', wanted_users=wanted_users, session_user=session_user)

@login_required
@app.route('/fetch_map', methods=["GET"])
def fetch_map():
    all_parsels = db.parsel
    return jsonify

@login_required
@app.route('/complaint', methods=["POST"])
def sikayet():
    if 'user_id' not in session:
        return redirect('/ziyaretci')
    
    title = request.form['title']
    content = request.form['content']
    dosya = request.files['fileupload']
    dosya_adi = dosya.filename
    complaint_case = str(uuid.uuid4())
    
    if allowed_file(dosya_adi):
        dosya.save('./static/webimgs/'+complaint_case+'.jpg')
        db.users.update_one(user, {
            "$push": { "complaint_photos": complaint_case }
        })
    else:
        return render_template('upload_error.html')
    
    db.complaints.insert_one({
        "_id": complaint_case,
        "title": title,
        "content": content,
        "comp_user": comp_user,
        "complainant": complainant
    })

    return render_template('complaint_sucess.html')

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
    if 'user_id' not in session:
        return redirect('/ziyaretci')
    user = get_user_from_id(user_id)
    if user == None:
        return render_template('404.html'), 404

    sameUser = isSameUser(user_id, user)

    return render_template('profile.html', user=user, sameUser=sameUser, project_name=project_name)

def isSameUser(user_id: str, user: dict) -> bool:
    if user_id == session['user_id']:
        sameUser = True
    else:
        sameUser = False
    return sameUser

@login_required
@app.route('/profile/', methods=["GET"])
def profile_user():
    if 'user_id' not in session:
        return redirect('/ziyaretci')
    user = get_session_user()

    return render_template("profile.html", user=user, sameUser=True, project_name=project_name)


@app.route('/profile/settings', methods=["GET"])
def profile_settings():
    if 'user_id' not in session:
        return redirect('/ziyaretci')
    user = get_session_user()

    return render_template('profile_settings.html', user=user, project_name=project_name)

@app.route('/profile/settings/update', methods=["POST"])
def profile_update():
    if 'user_id' not in session:
        return redirect('/ziyaretci')
    else:
        user = get_session_user()
    username = request.form['username']
    email = request.form['email']
    adaNo = request.form['adaNo']
    parselNo = request.form['parselNo']
    ilTercihi = request.form['ilTercihi']

    # encode password
    password = request.form['password']

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        update_dict = {
            "$set": {
                "username": username,
                "email": email,
                "adaNo": adaNo,
                "parselNo": parselNo,
                "il": ilTercihi
            }
        }
        db.users.update_one(user, update_dict)
        return render_template('profile_settings_success.html')
    else:
        return render_template('profile_settings_error.html')

@app.route('/sikayet/<string:comp_user_id>', methods=["GET", "POST"])
def complaint_ui(comp_user_id):
    if 'user_id' not in session:
        return redirect('/ziyaretci')
    user = get_session_user()
    return render_template('complaint.html', user=user, sikayet=get_user_from_id(comp_user_id), project_name=project_name)

def get_user_from_id(user_id):
    return db.users.find_one({
        "_id": user_id
    })

@app.route('/login', methods=['POST'])
def login():
    # Get the user's information from the request
    email = request.form['email']
    password = request.form['password']

    # Retrieve the user from the database
    user = db.users.find_one({'email': email})

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
        return render_template('signup.html', project_name=project_name)

@app.route('/giris', methods=["GET"])
def giris():
    if request.method == "GET":
        return render_template('login.html', project_name=project_name)

def allowed_file(filename):
    return ('.' in filename) and (filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)

@app.route('/ziyaretci')
@app.route('/', methods = ["GET"])
def guest():
    if 'user_id' in session:
        return redirect('/home')
    return render_template('guest.html', project_name=project_name)

@login_required
@app.route('/home')
@app.route('/home/', methods=['GET', 'POST'])
def index():
    # if 'user_id' not in session:
    #     return redirect('/ziyaretci')
    user = get_session_user()
    if request.method == 'POST':
        dosya = request.files['dosya']
        dosya_adi = dosya.filename
        case_id = str(uuid.uuid4())
        if allowed_file(dosya_adi):
            dosya.save('./static/webimgs/'+case_id+'.png')
            db.users.update_one(user, {
                "$push": { "user_photos": case_id }
            })
        else:
            return render_template('upload_error.html')
    return render_template('index.html', user=user, project_name=project_name)

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
    with pymongo.MongoClient(db_link, tlsCAFile=cacert) as client:
        collection_db = client["galbul"]
        db = collection_db.parsel

        response = db.insert_one(obj)
        if response == None:
            raise ValueError("Database cannot get accessable or not good. :D")

@app.route('/logo.png')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'logo.png',mimetype='image/png')


if __name__ == "__main__":
    
    
    app.run(host='0.0.0.0', port=8081, debug=1)