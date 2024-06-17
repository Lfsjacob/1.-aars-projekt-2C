import sqlite3

import flask

app = flask.Flask(__name__)

master_key = "Tagpap123"

def match(produktinfo, tablename):
    new = 0
    try:
        conn = sqlite3.connect(database="GTV_Tagdækning_ApS.db")
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM {tablename}')
        results = cur.fetchall()
        if tablename != "Bestillingsoversigt":
            for result in results:
                if result[1] == produktinfo[0] and result[4] == produktinfo[3]:
                    add_to_product(result[0], int(result[3] + int(produktinfo[2])), tablename)
                    new = 1
                    break
        if new == 0:
            add_new_product(produktinfo, tablename)
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
    print(f"Forsøger at slette produktid {id} i {tablename}")
    try:
        print("Åbner databasen")
        conn = sqlite3.connect(database="GTV_Tagdækning_ApS.db")
        query = f"""DELETE FROM {tablename} WHERE ID = ? """
        data = (id,)

        try:
            print("Forsøger at slette")
            cur = conn.cursor()
            cur.execute(query, data)
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            print(f"delete_amount:  Kunne ikke slette!: {e}")
        except Exception as e:
            print(f"Der skete en fejl: {e}")

    except sqlite3.Error as e:
        conn.rollback()
        print(f"Kunne ikke slette!: {e}")

@app.route('/home', methods=['POST', 'GET'])
def home():
    return flask.render_template("index.html")

@app.route('/lager', methods=['GET'])
def lager_get():
    data_rows = []
    conn = sqlite3.connect(database='GTV_Tagdækning_ApS.db')
    QUERY = "SELECT ID, Produktnavn, Produktnummer, Antal, Mål, Producent, Produktkategori, Pris FROM Lageroversigt ORDER BY id ASC"

    try:
        cur = conn.cursor()
        cur.execute(QUERY)
        data_rows = cur.fetchall()
    except sqlite3.OperationalError as oe:
        print(f"Transaction could not be processed: {oe}")
    except sqlite3.IntegrityError as ie:
        print(f"Integrity constraint violated: {ie}")
    except sqlite3.ProgrammingError as pe:
        print(f"You used the wrong SQL table: {pe}")
    except sqlite3.Error as e:
        print(f"Error calling SQL: {e}")
    finally:
        cur.close()
        conn.close()
    return flask.render_template('lager.html', data_rows = data_rows)

@app.route('/lager', methods=['POST'])
def lager_post():

    produktnavn = flask.request.form.get('produktnavn')
    produktnummer = flask.request.form.get('produktnummer')
    antal = flask.request.form.get('antal')
    længde = flask.request.form.get('længde')
    længde_enhed = flask.request.form.get('længde_enhed')
    if længde_enhed == "m":
        længde = "%.2f" % float(længde)
    bredde = flask.request.form.get('bredde')
    bredde_enhed = flask.request.form.get('bredde_enhed')
    if bredde_enhed == "m":
        bredde = "%.2f" % float(bredde)
    mål = f"B: {bredde} {bredde_enhed} L: {længde} {længde_enhed}"
    producent = flask.request.form.get('producent')
    produktkategori = flask.request.form.get('produktkategori')
    pris = f"{flask.request.form.get('pris')} kr."
    produktinfo = [produktnavn, produktnummer, antal, mål, producent, produktkategori, pris]
    
    if produktnavn is not None:
        match(produktinfo, "Lageroversigt")
    
    if produktnavn is None:
        id = flask.request.form.get('fjern_vare')
        delete_amount(id, "Lageroversigt")

    return lager_get()

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

@app.route('/register', methods=["GET", "POST"])
def register():
	global master_key
	received_key = flask.request.form.get('master_password')
	if flask.request.method == "POST" and received_key == master_key:
		username = flask.request.form.get('brugernavn')
		password = flask.request.form.get('password')
		print(f"{username = }")
		print(f"{password = }  ")
		try:
			conn = sqlite3.connect(database="GTV_Tagdækning_ApS.db")
			cur = conn.cursor()
			query = f"INSERT INTO Users(Username, Password) VALUES(?, ?)"
			data = (username, password)
			cur.execute(query, data)
			conn.commit()
		except sqlite3.Error as e:
			conn.rollback()
			print(f"Kunne ikke oprette {e}")

	return flask.render_template("register.html")


@app.route("/", methods=["GET", "POST"])
def login():
    if flask.request.method == "POST":
        username = flask.request.form.get('brugernavn')
        password = flask.request.form.get('password')
        conn= sqlite3.connect(database="GTV_Tagdækning_ApS.db")
        cur = conn.cursor()
        query = f"SELECT * FROM Users"
        cur.execute(query)
        results = cur.fetchall()
        for row in results:
            if row[1] == username and row[2] == password:
                return flask.render_template("index.html")
    return flask.render_template("login.html")
    
if __name__ == "__main__":
    app.run(host="0.0.0.0")