import time
import sqlite3

import flask

app = flask.Flask(__name__)



@app.route('/', methods=['POST', 'GET'])
def home():
    return flask.render_template("base.html")

@app.route('/lager', methods=['POST', 'GET'])
def lager():
    return flask.render_template("lager.html")

@app.route('/bestilte_varer', methods=['POST', 'GET'])
def bestilte_varer():
    produktnavn = flask.request.form.get('pnavn')
    produktnummer = flask.request.form.get('EAN')
    antal = flask.request.form.get('antal')
    bredde = flask.request.form.get('bredde')
    bredde_enhed = flask.request.form.get('benhed')
    længde = flask.request.form.get('længde')
    længde_enhed = flask.request.form.get('lenhed')
    mål = f"B:{bredde} {bredde_enhed} L:{længde}{længde_enhed}"
    producent = flask.request.form.get('producent')
    produktkategori = flask.request.form.get('pkategori')
    pris = flask.request.form.get('pris')
    produktinfo = [produktnavn, produktnummer, antal, mål, producent,produktkategori, pris]
    print(produktinfo)
    return flask.render_template("bestilte_varer.html")

@app.route('/prisliste', methods=['POST', 'GET'])
def prisliste():
    return flask.render_template("prisliste.html")