from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from werkzeug.security import check_password_hash

login_bp = Blueprint('login', __name__)

# MongoDB setup
uri = "mongodb+srv://caciusa:0500868021Yaw@cluster0.ca1fcqn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["caciusa"]
users_collection = db["users"]

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = users_collection.find_one({"username": username})
        if user and check_password_hash(user["password"], password):
            session["user"] = username
            session["role"] = user.get("role", "admin")
            flash("✅ Login successful", "success")
            return redirect(url_for("admin_dashboard.admin_dashboard"))  # fixed endpoint reference
        else:
            flash("❌ Invalid username or password", "danger")

    return render_template("login.html")

@login_bp.route("/logout")
def logout():
    session.clear()
    flash("🚪 Logged out successfully", "info")
    return redirect(url_for("login.login"))
