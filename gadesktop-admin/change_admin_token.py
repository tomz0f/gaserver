from pymongo import MongoClient
from dotenv import load_dotenv
import os
import random
from uuid import uuid4 as random_gen
load_dotenv()

DB_URI = os.getenv('DB_URI')
ADMIN_DB_COLLECTION = os.getenv('ADMIN_DB_COLLECTION')
with MongoClient(DB_URI) as client:
    db = client.galbul
    collection = db['users']
    gen_secret = ""
    for i in range(random.randint(10,32)):
        gen_secret += str(random_gen())
    
    db[ADMIN_DB_COLLECTION].delete_many({})
    db[ADMIN_DB_COLLECTION].insert_one({
        "secretKey": gen_secret
    })