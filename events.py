from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
from bson import ObjectId
from db import events_collection
import json

events_bp = Blueprint('events', __name__)

# Helper: Delete past events
def delete_past_events():
    # Use full datetime object with time set to 00:00:00
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    events_collection.delete_many({'event_date': {'$lt': today}})

# Add new event
@events_bp.route('/add-event', methods=['GET', 'POST'])
def add_event():
    delete_past_events()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        image_url = request.form.get('image_url', '').strip()
        event_date_str = request.form.get('event_date', '')
        created_at = datetime.utcnow()

        try:
            event_date = datetime.strptime(event_date_str, '%Y-%m-%d')  # keep as datetime
        except ValueError:
            flash('❌ Invalid date format.', 'danger')
            return redirect(url_for('events.add_event'))

        events_collection.insert_one({
            'title': title,
            'description': description,
            'image_url': image_url,
            'event_date': event_date,
            'created_at': created_at
        })

        flash('✅ Event added successfully!', 'success')
        return redirect(url_for('events.add_event'))

    events = list(events_collection.find().sort('created_at', -1))
    return render_template('addevent.html', events=events)

# Edit event
@events_bp.route('/edit-event/<event_id>', methods=['POST'])
def edit_event(event_id):
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    image_url = request.form.get('image_url', '').strip()
    event_date_str = request.form.get('event_date', '')

    try:
        event_date = datetime.strptime(event_date_str, '%Y-%m-%d')  # keep as datetime
    except ValueError:
        flash('❌ Invalid date format.', 'danger')
        return redirect(url_for('events.add_event'))

    events_collection.update_one(
        {'_id': ObjectId(event_id)},
        {'$set': {
            'title': title,
            'description': description,
            'image_url': image_url,
            'event_date': event_date
        }}
    )

    flash('✏️ Event updated successfully.', 'info')
    return redirect(url_for('events.add_event'))

# Delete event
@events_bp.route('/delete-event/<event_id>')
def delete_event(event_id):
    events_collection.delete_one({'_id': ObjectId(event_id)})
    flash('🗑️ Event deleted.', 'danger')
    return redirect(url_for('events.add_event'))

# Display event page
@events_bp.route('/events')
def show_events():
    delete_past_events()

    events = list(events_collection.find().sort('event_date', 1))

    # Prepare JSON for FullCalendar
    calendar_events = []
    for event in events:
        if event.get('event_date'):
            calendar_events.append({
                'title': event.get('title', ''),
                'description': event.get('description', ''),
                'start': event['event_date'].strftime('%Y-%m-%d')
            })

    return render_template('events.html', events=events, events_json=json.dumps(calendar_events))
