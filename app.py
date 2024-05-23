from flask import Flask, render_template, request


app = Flask(__name__)

# Functions
def get_variables():
    x = request.form.get('første_variabel')
    return x

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lager', methods = ['POST', 'GET'])
def lager():
    første_variabel = None
    if request.method == 'POST':
        første_variabel = get_variables()
    return render_template('lager.html', første_variabel = første_variabel)

@app.route('/bestilte_varer')
def bestilte_varer():
    return render_template('bestilte_varer.html')

@app.route('/prisliste')
def prisliste():
    return render_template('prisliste.html')


app.run(debug=True)