from flask import Blueprint, render_template, request, redirect, flash, url_for
from bson import ObjectId
from datetime import datetime
from db import db

gallery_bp = Blueprint("gallery", __name__)
gallery_collection = db["gallery"]

# ========== Add & View Gallery Images (on same page) ==========
@gallery_bp.route('/add-gallery', methods=['GET', 'POST'])
def add_gallery():
    if request.method == 'POST':
        description = request.form.get('description', '').strip()
        date_str = request.form.get('date', '').strip()
        image_url = request.form.get('image_url', '').strip()

        # Handle album input: either select or new
        selected_album = request.form.get('album_select')
        new_album = request.form.get('album_new', '').strip()
        album = new_album if selected_album == "__new__" else selected_album or None

        if not description or not date_str or not image_url:
            flash("❌ All fields except album are required.", "danger")
            return redirect(url_for("gallery.add_gallery"))

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            flash("❌ Invalid date format.", "danger")
            return redirect(url_for("gallery.add_gallery"))

        gallery_collection.insert_one({
            "description": description,
            "date": date,
            "image_url": image_url,
            "album": album,
            "timestamp": datetime.utcnow()
        })

        flash("✅ Gallery image added successfully!", "success")
        return redirect(url_for("gallery.add_gallery"))

    # Build album list for dropdown and organize images by album
    albums_dict = {}
    album_names = set()

    for item in gallery_collection.find().sort("timestamp", -1):
        key = item.get("album") or "Ungrouped"
        album_names.add(key)
        albums_dict.setdefault(key, []).append(item)

    return render_template("add_gallery.html", albums=albums_dict, album_names=sorted(album_names))


# ========== View Gallery Page ==========
@gallery_bp.route('/gallery')
def view_gallery():
    albums = {}
    for item in gallery_collection.find().sort("timestamp", -1):
        item['date_str'] = item['date'].strftime("%B %d, %Y")
        key = item.get("album") or "Photo"
        albums.setdefault(key, []).append(item)
    return render_template("gallery.html", albums=albums)


# ========== Delete Gallery Image ==========
@gallery_bp.route('/delete-gallery/<image_id>')
def delete_gallery(image_id):
    try:
        gallery_collection.delete_one({"_id": ObjectId(image_id)})
        flash("🗑️ Image deleted from gallery.", "danger")
    except Exception as e:
        flash(f"❌ Error deleting image: {e}", "danger")
    return redirect(url_for("gallery.add_gallery"))
