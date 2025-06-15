from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
from bson import ObjectId
from db import contact_collection, locations_collection

contact_bp = Blueprint('contact', __name__)

# =============== Contact Form + Locations Display ===============
@contact_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        if not name or not email or not message:
            flash('❌ Please fill out all fields.', 'danger')
            return redirect(url_for('contact.contact'))

        contact_collection.insert_one({
            'name': name,
            'email': email,
            'message': message,
            'timestamp': datetime.utcnow(),
            'read': False
        })

        flash('✅ Thank you! Your message has been sent to CACI-USA. 🙏', 'success')
        return redirect(url_for('contact.contact'))

    # Fetch locations to display on the contact page
    locations = list(locations_collection.find().sort("timestamp", -1))
    return render_template('contact.html', locations=locations)

# =============== Messages ============
@contact_bp.route('/messages')
def view_messages():
    messages = list(contact_collection.find().sort("timestamp", -1))
    return render_template('messages.html', messages=messages)

@contact_bp.route('/mark-read/<message_id>')
def mark_read(message_id):
    try:
        contact_collection.update_one(
            {'_id': ObjectId(message_id)},
            {'$set': {'read': True}}
        )
        flash('🟢 Message marked as replied.', 'info')
    except Exception as e:
        flash(f'❌ Failed to mark as replied: {e}', 'danger')
    return redirect(url_for('contact.view_messages'))

@contact_bp.route('/delete-message/<message_id>')
def delete_message(message_id):
    try:
        contact_collection.delete_one({'_id': ObjectId(message_id)})
        flash('🗑️ Message deleted.', 'danger')
    except Exception as e:
        flash(f'❌ Failed to delete message: {e}', 'danger')
    return redirect(url_for('contact.view_messages'))

# =============== Add Church Location ===============
@contact_bp.route('/add-location', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        address = request.form.get('address', '').strip()
        phone = request.form.get('phone', '').strip()
        assembly = request.form.get('assembly', '').strip()
        image_url = request.form.get('image_url', '').strip()

        if not name or not address or not phone or not assembly or not image_url:
            flash('❌ All fields are required.', 'danger')
            return redirect(url_for('contact.add_location'))

        locations_collection.insert_one({
            'name': name,
            'address': address,
            'phone': phone,
            'assembly': assembly,
            'image_url': image_url,
            'timestamp': datetime.utcnow()
        })

        flash('✅ Location added successfully!', 'success')
        return redirect(url_for('contact.add_location'))

    locations = list(locations_collection.find().sort("timestamp", -1))
    return render_template('add_locations.html', locations=locations)

# =============== Update Church Location ===============
@contact_bp.route('/update-location/<location_id>', methods=['POST'])
def update_location(location_id):
    try:
        updated_data = {
            'name': request.form.get('name', '').strip(),
            'address': request.form.get('address', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'assembly': request.form.get('assembly', '').strip(),
            'image_url': request.form.get('image_url', '').strip(),
            'timestamp': datetime.utcnow()
        }

        if not all(updated_data.values()):
            flash('❌ All fields are required.', 'danger')
            return redirect(url_for('contact.add_location'))

        locations_collection.update_one({'_id': ObjectId(location_id)}, {'$set': updated_data})
        flash("✅ Location updated successfully.", "success")
    except Exception as e:
        flash(f"❌ Failed to update location: {e}", "danger")

    return redirect(url_for('contact.add_location'))

# =============== Delete Church Location ===============
@contact_bp.route('/delete-location/<location_id>')
def delete_location(location_id):
    try:
        locations_collection.delete_one({'_id': ObjectId(location_id)})
        flash('🗑️ Location deleted.', 'danger')
    except Exception as e:
        flash(f'❌ Failed to delete location: {e}', 'danger')
    return redirect(url_for('contact.add_location'))
