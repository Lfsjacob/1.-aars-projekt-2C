from flask import Flask, render_template, request, url_for, session
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'your_secret_key_here'

# Bruger Login-database
user = {
    'user1': {
        'username': 'user1',
        'password': bcrypt.generate_password_hash('password1').decode(utf-8)
    },
    'user2': {
        'username': 'user2',
        'password': bcrypt.generate
    }
}