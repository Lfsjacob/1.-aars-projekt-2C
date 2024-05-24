from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Macking"

app.run(debug=True)