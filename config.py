import os

key = os.environ.get("SECRET_KEY")
db_url = os.environ.get("DB_URL")
class Config(object):
   SECRET_KEY = "yigitinsifresi"
   DB_URI = "mongodb+srv://yigit:yigitinsifresi@projectdatabasegalbul.ixx82u7.mongodb.net/test"
