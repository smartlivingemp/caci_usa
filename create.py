from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from werkzeug.security import generate_password_hash

# --- MongoDB URI ---
uri = "mongodb+srv://caciusa:0500868021Yaw@cluster0.ca1fcqn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# --- Connect to MongoDB ---
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["caciusa"]
users_collection = db["users"]

# --- Hardcoded admin credentials ---
username = "emmanuel"
password = "emmanuel@caciusa.org"

# --- Check if user exists ---
if users_collection.find_one({"username": username}):
    print("❗ User already exists.")
else:
    hashed_pw = generate_password_hash(password)
    users_collection.insert_one({
        "username": username,
        "password": hashed_pw,
        "role": "admin"
    })
    print("✅ Admin user created successfully.")
