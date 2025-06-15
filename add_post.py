from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from bson import ObjectId
from db import blog_collection  # Ensure your db.py defines this properly

add_post_bp = Blueprint('add_post', __name__)

@add_post_bp.route('/add-post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image_url = request.form.get('image_url', '')  # Optional
        posted_by = request.form.get('posted_by', 'Anonymous')  # New field

        blog_collection.insert_one({
            'title': title,
            'description': description,
            'image_url': image_url,
            'posted_by': posted_by,
            'created_at': datetime.utcnow()
        })

        flash('✅ News post added successfully!', 'success')
        return redirect(url_for('add_post.add_post'))

    posts = list(blog_collection.find().sort('created_at', -1))
    return render_template('addpost.html', posts=posts)

@add_post_bp.route('/edit-post/<post_id>', methods=['POST'])
def edit_post(post_id):
    blog_collection.update_one({'_id': ObjectId(post_id)}, {
        '$set': {
            'title': request.form['title'],
            'description': request.form['description'],
            'image_url': request.form.get('image_url', ''),
            'posted_by': request.form.get('posted_by', 'Anonymous')  # Include edit for posted_by
        }
    })
    flash('✏️ Post updated successfully.', 'info')
    return redirect(url_for('add_post.add_post'))

@add_post_bp.route('/delete-post/<post_id>')
def delete_post(post_id):
    blog_collection.delete_one({'_id': ObjectId(post_id)})
    flash('🗑️ Post deleted.', 'danger')
    return redirect(url_for('add_post.add_post'))

@add_post_bp.route('/blog')
def blog():
    posts = list(blog_collection.find().sort('created_at', -1))
    return render_template('blog.html', posts=posts)
