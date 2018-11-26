from flask import Flask
from flask import render_template
app = Flask(import_name=__name__)

@app.route('/')
def index():
    return 'Index Page'

# @app.route('/hello')
# def hello():
#     return 'Hello World'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)