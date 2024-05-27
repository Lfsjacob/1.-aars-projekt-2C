from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
       return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
        return render_template('register.html')
    
app.run(debug=True)