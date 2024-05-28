import sqlite3

import flask

app = flask.Flask(__name__)

def match(produktinfo, tablename):
    print("Tjekker rute")
    new = 0
    route = tablename
    try:
        conn = sqlite3.connect(database="GTV_Tagdækning_ApS.db")
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM {tablename}')
        # for row in cur:
        results = cur.fetchall()
        for result in results:
            print(f"{result[0]} {result[1] = }  {result[4] = }")
            if result[1] == produktinfo[0] and result[4] == produktinfo[3]:
                print(f"{produktinfo[2] = }")
                add_to_product(result[0], int(result[3] + int(produktinfo[2])), tablename)
                print("JA!")
                conn.commit()
                new = 1
                break
        if new == 0:
            add_new_product(produktinfo, tablename)
        print(results)
        conn.commit()
    except Exception as e:
        print(f"Der skete en fejl: {e}")

def add_to_product(id, antal, tablename):
    print("Forsøger at tilføje til produkt")
    try:
        print("Åbner databasen")
        conn = sqlite3.connect(database="GTV_Tagdækning_ApS.db")
        query = f"""UPDATE {tablename} SET Antal = ? WHERE ID = ?"""
        data = antal, id

        try:
            print("Forsøger at indsætte")
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

def add_new_product(produktinfo, tablename):
    print("Forsøger at indsætte nyt produkt")
    try:
        print("Åbner databasen")
        conn = sqlite3.connect(database="GTV_Tagdækning_ApS.db")
        query = f"""INSERT INTO {tablename}(Produktnavn, Produktnummer, Antal, Mål, Producent, Produktkategori, Pris) VALUES(?, ?, ?, ?, ?, ?, ?)"""
        data = tuple(produktinfo)
        try:
            print("Forsøger at indsætte")
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

def delete_amount(id, tablename):
    print(f"Forsøger at sætte {id} i {tablename} til 0")
    try:
        print("Åbner databasen")
        conn = sqlite3.connect(database="GTV_Tagdækning_ApS.db")
        query = f"""UPDATE {tablename} SET Antal = ? WHERE ID = ?"""
        data = 0, id

        try:
            print("Forsøger at indsætte")
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

@app.route('/', methods=['POST', 'GET'])
def home():
    return flask.render_template("tester.html")

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
    

    
    if produktnavn is None:
        id = int(flask.request.form.get('fjern_vare'))
        try:
            conn = sqlite3.connect(database="GTV_Tagdækning_ApS.db")
            query = f"""SELECT Produktnavn, Produktnummer, Antal, Mål, Producent, Produktkategori, Pris FROM Bestillingsoversigt WHERE ID = ?"""
            data = id
            cur = conn.cursor()
            cur.execute(query, (data,))
            conn.commit
            results = cur.fetchall()
            result = results[0]
            print(f"{result = }")
            match(list(result), "Lageroversigt")
            delete_amount(id, "Bestillingsoversigt")
        except Exception as e:
                print(f"bvtl   Der skete en fejl: {e}")
        

    else:
        match(produktinfo, "Bestillingsoversigt")

    return bestilte_varer()
    

@app.route('/prisliste', methods=['POST', 'GET'])
def prisliste():
    return flask.render_template("prisliste.html")

@app.route('/test', methods=['POST', 'GET'])
def test_site():
    return flask.render_template("tester.html")