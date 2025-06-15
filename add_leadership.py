from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import leadership_collection
from bson import ObjectId

add_leadership_bp = Blueprint('add_leadership', __name__)

@add_leadership_bp.route('/add-leadership', methods=['GET', 'POST'])
def add_leadership():
    if request.method == 'POST':
        name = request.form.get('name')
        position = request.form.get('position')
        image_url = request.form.get('image_url')
        leader_id = request.form.get('leader_id')

        if name and position and image_url:
            if leader_id:  # Editing existing
                leadership_collection.update_one(
                    {'_id': ObjectId(leader_id)},
                    {'$set': {'name': name, 'position': position, 'image_url': image_url}}
                )
                flash('Leader updated successfully!', 'success')
            else:  # New leader
                leadership_collection.insert_one({
                    'name': name,
                    'position': position,
                    'image_url': image_url
                })
                flash('Leader added successfully!', 'success')
        else:
            flash('Please fill all fields.', 'danger')

        return redirect(url_for('add_leadership.add_leadership'))

    leaders = leadership_collection.find()
    return render_template('add_leadership.html', leaders=leaders)

@add_leadership_bp.route('/delete-leader/<leader_id>', methods=['GET'])
def delete_leader(leader_id):
    leadership_collection.delete_one({'_id': ObjectId(leader_id)})
    flash('Leader deleted successfully.', 'success')
    return redirect(url_for('add_leadership.add_leadership'))
