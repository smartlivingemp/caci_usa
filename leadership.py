from flask import Blueprint, render_template
from pymongo import MongoClient

# Define blueprint
leadership_bp = Blueprint('leadership', __name__)

# Connect to MongoDB
client = MongoClient("mongodb+srv://caciusa:0500868021Yaw@cluster0.ca1fcqn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["caciusa"]
collection = db["leadership"]

# Route to display leadership profiles
@leadership_bp.route('/leadership')
def leadership_page():
    leaders = list(collection.find())
    return render_template('leadership.html', leaders=leaders)
