from flask import Flask
import request
from flask import render_template
app = Flask(__name__)


def valid_login(user,passwd):
    if user == "a" and passwd == "b":
        return True
    else:
        return False

def log_the_user_in(user):
    return "Login successfu!"

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)

if __name__ == '__main__':

    app.run(host='0.0.0.0',port=8081)
