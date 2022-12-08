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
from functools import wraps
from werkzeug.utils import secure_filename
import pymongo
db_link = "mongodb+srv://yigit:yigitinsifresi@projectdatabasegalbul.ixx82u7.mongodb.net/test"
client = pymongo.MongoClient(db_link)
db = client.user_login_system

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'
#################################
##### I'M WORTHLESS GUY :') #####
#################################

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ERR_CODES = [400, 401, 403, 404, 500, 502, 503, 504]

def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap

from user import routes

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/kayit', methods = ["GET", "POST"])
def kayit():
    if request.method == "GET":
        return render_template('signup.html')

    if request.method == "POST":
        return render_template('redirect_index.html')

@app.route('/giris', methods=["GET", "POST"])
def giris():
    if request.method == "GET":
        return render_template('login.html')

    if request.method == "POST":

        return render_template('redirect_index.html')
def allowed_file(filename):
    return ('.' in filename) and (filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        dosya = request.files['dosya']
        dosya_adi = dosya.filename
        if allowed_file(dosya_adi):
            dosya.save('webimgs/'+dosya_adi)
        else:
            return render_template('upload_error.html')
    return render_template('index.html')

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
