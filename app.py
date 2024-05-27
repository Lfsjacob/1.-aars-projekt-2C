import sqlite3

import flask

app = flask.Flask(__name__)

def match(produktnavn, produktnummer, antal, mål, producent,produktkategori, pris):
    produktnavn = produktnavn
    antal = antal
    mål = mål
    new = 0
    try:
        conn = sqlite3.connect(database="GTV_Tagdækning_ApS.db")
        cur = conn.cursor()
        cur.execute('SELECT * FROM Bestillingsoversigt')
        # for row in cur:
        results = cur.fetchall()
        for result in results:
            print(f"{result[0]} {result[1] = }  {result[4] = }")
            if result[1] == produktnavn and result[4] == mål:
                print(f"{antal = }")
                add_to_product(result[0], int(result[3] + int(antal)))
                print("JA!")
                conn.commit()
                new = 1
                break
        if new == 0:
            add_new_product(produktnavn, produktnummer, antal, mål, producent,produktkategori, pris)
        print(results)
        conn.commit()
    except Exception as e:
        print(f"Der skete en fejl: {e}")


def add_to_product(id, antal):
    try:
        conn = sqlite3.connect(database="GTV_Tagdækning_ApS.db")
        query = f"""UPDATE Bestillingsoversigt SET Antal = ? WHERE ID = ?"""
        data = antal, id

        try:
            cur = conn.cursor()
            cur.execute(query, data)
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            print(f"add_to_product:  Kunne ikke indsætte!: {e}")
        except Exception as e:
            print(f"Der skete en fejl: {e}")

    except sqlite3.Error as e:
        conn.rollback()
        print(f"Kunne ikke indsætte!: {e}")

def add_new_product(produktnavn, produktnummer, antal, mål, producent, produktkategori, pris):
    try:
        conn = sqlite3.connect(database="GTV_Tagdækning_ApS.db")
        query = """INSERT INTO Bestillingsoversigt(Produktnavn, Produktnummer, Antal, Mål, Producent, Produktkategori, Pris) VALUES(?, ?, ?, ?, ?, ?, ?)"""
        data = produktnavn, produktnummer, antal, mål, producent, produktkategori, pris

        try:
            cur = conn.cursor()
            cur.execute(query, data)
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Overordnet:  Kunne ikke indsætte!: {e}")
        except Exception as e:
            print(f"Der skete en fejl: {e}")

    except sqlite3.Error as e:
        conn.rollback()
        print(f"Kunne ikke indsætte!: {e}")

def bestilling_til_lager():
    conn = sqlite3.connect(database="GTV_Tagdækning_ApS.db")
    query = """"""

@app.route('/', methods=['POST', 'GET'])
def home():
    return flask.render_template("base.html")

@app.route('/lager', methods=['POST', 'GET'])
def lager():
    return flask.render_template("lager.html")

@app.route('/bestilte_varer', methods=['GET'])
def bestilte_varer():
    try:
        conn = sqlite3.connect(database="GTV_Tagdækning_ApS.db")
        cur = conn.cursor()
        cur.execute("""SELECT ID, Produktnavn, Produktnummer, Antal, Mål, Producent, Produktkategori, Pris FROM Bestillingsoversigt ORDER BY Produktkategori ASC""")
    except Exception as e:
            print(f"Der skete en fejl: {e}")
    return flask.render_template("bestilte_varer.html", items=cur.fetchall())

@app.route('/bestilte_varer', methods=['POST'])
def bestilte_varer_post():
    produktnavn = flask.request.form.get('pnavn')
    produktnummer = flask.request.form.get('EAN')
    antal = flask.request.form.get('antal')
    bredde = flask.request.form.get('bredde')
    bredde_enhed = flask.request.form.get('benhed')
    if bredde_enhed == "m":
        bredde = "%.2f" % float(bredde)
    længde = flask.request.form.get('længde')
    længde_enhed = flask.request.form.get('lenhed')
    if længde_enhed == "m":
        længde = "%.2f" % float(længde)
    mål = f"B: {bredde} {bredde_enhed} L: {længde} {længde_enhed}"
    producent = flask.request.form.get('producent')
    produktkategori = flask.request.form.get('pkategori')
    pris = f"{flask.request.form.get('pris')} kr."
    produktinfo = [produktnavn, produktnummer, antal, mål, producent,produktkategori, pris]
    print(produktinfo)
    
    match(produktnavn, produktnummer, antal, mål, producent,produktkategori, pris)

    return bestilte_varer()

@app.route('/prisliste', methods=['POST', 'GET'])
def prisliste():
    return flask.render_template("prisliste.html")