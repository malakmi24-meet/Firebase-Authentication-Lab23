from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

const = {
  "apiKey": "AIzaSyBWctJg8ZK8VZNXrg9gg88rHURsFknKQEo",
  "authDomain": "testing-firebase-21610.firebaseapp.com",
  "projectId": "testing-firebase-21610",
  "storageBucket": "testing-firebase-21610.appspot.com",
  "messagingSenderId": "173491177343",
  "appId": "1:173491177343:web:58e99d4e0ac08d7b2dbc4a",
  "databaseURL": ""
};

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if len(password) < 6:
            print('Password too short.')
        else:
            return render_template("signin.html")
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)