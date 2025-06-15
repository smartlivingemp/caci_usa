from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from db import popup_collection  # Shared DB connection

home_popup_bp = Blueprint('home_popup', __name__)

@home_popup_bp.route('/home-popup', methods=['GET', 'POST'])
def home_popup():
    if request.method == 'POST':
        image_url = request.form.get('image_url')
        if image_url:
            popup_collection.delete_many({})  # Keep only one popup
            popup_collection.insert_one({
                'image_url': image_url,
                'updated_at': datetime.utcnow()
            })
            flash("Popup image updated!", "success")
        else:
            flash("Image upload failed. Please try again.", "danger")
        return redirect(url_for('home_popup.home_popup'))

    current = popup_collection.find_one()
    return render_template('home_popup.html', current=current)

# Optional: Reusable function to fetch popup image (for index.html or layout.html)
def get_current_popup():
    return popup_collection.find_one()
