import sqlite3
import logging
import sys

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

db_total_connections = 0


# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    global db_total_connections
    db_total_connections += 1
    app.logger.debug('Metrics request successfull')
 
    return post

# Function to get the number of posts at DB
def get_post_count():
    connection = get_db_connection()
    post_count = connection.execute('SELECT count(*) from posts').fetchone()[0]
    connection.close()
    global db_total_connections
    db_total_connections += 1
    return post_count


# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.error('Article not found!')
      return render_template('404.html'), 404
    else:
      post_title = post[2]
      app.logger.info('Article \"' + str(post_title) + '\" retrieved!')
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('About us retrieved!')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            app.logger.info('New article created!')
            return redirect(url_for('index'))

    return render_template('create.html')


# Health Status
@app.route('/healthz')
def healthz():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    return response

# Metrics Page
@app.route('/metrics')
def metrics():
    post_count = get_post_count()
    response = app.response_class(
            response=json.dumps({"db_connection_count":db_total_connections,"post_count":post_count}),
            status=200,
            mimetype='application/json'
    )
    app.logger.info('Metrics request successfull!')
    return response

# start the application on port 3111
if __name__ == "__main__":

   # Logging implementation from https://stackoverflow.com/questions/14058453/making-python-loggers-output-all-messages-to-stdout-in-addition-to-log-file
   logger = logging.getLogger('')
   logger.setLevel(logging.WARNING)

   formatter = logging.Formatter('%(levelname)s:%(filename)s:%(asctime)s %(message)s', datefmt='%d/%m/%Y, %H:%M:%S,')

   stdout_handler = logging.StreamHandler(sys.stdout)
   stderr_handler = logging.StreamHandler(sys.stderr)

   stdout_handler.setFormatter(formatter)
   stderr_handler.setFormatter(formatter)
   logger.addHandler(stdout_handler)
   logger.addHandler(stderr_handler)

   # Start App
   app.run(host='0.0.0.0', port='3111')
