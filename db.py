from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://caciusa:0500868021Yaw@cluster0.ca1fcqn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))
db = client['caciusa']  # Database
leadership_collection = db['leadership']
popup_collection = db["home_popup"]
blog_collection= db["blog"]
events_collection= db["events"]
contact_collection = db['contact_messages']
locations_collection = db['Locations']
visits_collection = db['visits']
gallery_collection = db["gallery"]



try:
    client.admin.command('ping')
    print("Connected to MongoDB!")
except Exception as e:
    print("MongoDB connection error:", e)
 