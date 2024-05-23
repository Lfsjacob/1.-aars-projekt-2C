from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lager')
def lager():
    return render_template('lager.html')

@app.route('/bestilte_varer')
def bestilte_varer():
    return render_template('bestilte_varer.html')

@app.route('/prisliste')
def prisliste():
    return render_template('prisliste.html')


app.run(debug=True)