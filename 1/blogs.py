import sqlite3
from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/blog')
def blog():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()

    # Fetch blog post data from the database
    cursor.execute('SELECT title, content, image, video FROM blog_posts')
    blog_posts = [{'title': row[0], 'content': row[1], 'image': row[2], 'video': row[3]} for row in cursor.fetchall()]

    conn.close()
    return render_template('blog.html', blog_posts=blog_posts)

@app.route('/publish', methods=['POST'])
def publish():
    title = request.form['title']
    content = request.form['content']
    image = request.files['image']
    video = request.files['video']

    # Save image and video files to the 'uploads' folder
    if image:
        image_filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_filename)
    else:
        image_filename = None

    if video:
        video_filename = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
        video.save(video_filename)
    else:
        video_filename = None

    # Insert the blog post data into the database
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO blog_posts (title, content, image, video)
        VALUES (?, ?, ?, ?)
    ''', (title, content, image_filename, video_filename))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
