from flask import Flask, render_template
from datetime import datetime
from leadership import leadership_bp
from add_leadership import add_leadership_bp
from home_popup import home_popup_bp
from db import popup_collection, visits_collection
from add_post import add_post_bp
from events import events_bp
from contact import contact_bp  # contact.py uses SendGrid via helper
from gallery import gallery_bp
from admin_dashboard import admin_dashboard_bp
from login import login_bp




app = Flask(__name__)
app.secret_key = 'c9d2d44210f7475e8bcbd2f7d062bdb926da355e8f3a96305e20cd4dff54ae3c'

# =======================
# Register Blueprints
# =======================
app.register_blueprint(leadership_bp)
app.register_blueprint(add_leadership_bp)
app.register_blueprint(home_popup_bp)
app.register_blueprint(add_post_bp)
app.register_blueprint(events_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(gallery_bp)
app.register_blueprint(admin_dashboard_bp)
app.register_blueprint(login_bp)



# =======================
# Routes
# =======================

@app.route('/')
def index():
    # Increment the visit counter
    today = datetime.utcnow().strftime('%Y-%m-%d')
    visits_collection.update_one(
        {'date': today},
        {'$inc': {'count': 1}},
        upsert=True
    )

    popup = popup_collection.find_one()
    return render_template('index.html', popup=popup)

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/ministry')
def ministry():
    return render_template('ministry.html')

# =======================
# Run App
# =======================
if __name__ == '__main__':
    app.run(debug=True)
