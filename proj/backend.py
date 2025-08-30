from flask import Flask, render_template, request, redirect, url_for, flash
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

USER_FILE = 'users.json'

def load_users():
    try:
        with open(USER_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=4)

users = load_users()
if not users:
    default_user = {"email": "user@example.com", "password": "careerbot123"}
    users.append(default_user)
    save_users(users)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    stored_users = load_users()
    user = next((u for u in stored_users if u['email'] == email and u['password'] == password), None)
    if user:
        return redirect(url_for('welcome'))
    else:
        flash('Invalid email or password.')
        return redirect(url_for('index'))

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    new_email = request.form['email']
    new_password = request.form['password']
    stored_users = load_users()
    if any(user['email'] == new_email for user in stored_users):
        flash('Email address already exists.')
        return redirect(url_for('signup_page'))
    else:
        stored_users.append({"email": new_email, "password": new_password})
        save_users(stored_users)
        flash('Account created successfully. Please log in.')
        return redirect(url_for('index'))

@app.route('/welcome')
def welcome():
    return "<h1>Welcome to CareerBot!</h1>"

if __name__ == '__main__':
    app.run(debug=True)