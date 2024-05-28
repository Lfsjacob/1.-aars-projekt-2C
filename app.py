from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)

# Functions
def match(produktnavn, produktnummer, antal, mål, producent,produktkategori, pris):
    produktnavn = produktnavn
    antal = antal
    mål = mål
    new = 0
    try:
        conn = sqlite3.connect(database="database/ny_database.db")
        cur = conn.cursor()
        cur.execute('SELECT * FROM Lageroversigt')
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
        conn = sqlite3.connect(database="database/ny_database.db")
        query = f"""UPDATE Lageroversigt SET Antal = ? WHERE ID = ?"""
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
        conn = sqlite3.connect(database="database/ny_database.db")
        query = """INSERT INTO Lageroversigt(Produktnavn, Produktnummer, Antal, Mål, Producent, Produktkategori, Pris) VALUES(?, ?, ?, ?, ?, ?, ?)"""
        query2 = "SELECT ID, Produktnavn, Produktnummer, Antal, Mål, Producent, Produktkategori, Pris FROM Lageroversigt ORDER BY id ASC"
        data = produktnavn, produktnummer, antal, mål, producent, produktkategori, pris

        try:
            cur = conn.cursor()
            cur.execute(query, data)
            conn.commit()
            # cur.execute(query2)
            # data_rows = cur.fetchall()
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Overordnet:  Kunne ikke indsætte!: {e}")
        except Exception as e:
            print(f"Der skete en fejl: {e}")

    except sqlite3.Error as e:
        conn.rollback()
        print(f"Kunne ikke indsætte!: {e}")

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lager', methods = ['POST', 'GET'])
def lager():
    data_rows = []
    conn = sqlite3.connect(database='database/ny_database.db')
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

    if request.method == 'POST':
        produktnavn = request.form.get('produktnavn')
        produktnummer = request.form.get('produktnummer')
        antal = request.form.get('antal')
        længde = request.form.get('længde')
        længde_enhed = request.form.get('længde_enhed')
        bredde = request.form.get('bredde')
        bredde_enhed = request.form.get('bredde_enhed')
        mål = f"B: {bredde} {bredde_enhed} L: {længde} {længde_enhed}"
        producent = request.form.get('producent')
        produktkategori = request.form.get('produktkategori')
        pris = request.form.get('pris')
       
        conn = sqlite3.connect(database='database/ny_database.db')
        query = "INSERT INTO Lageroversigt(Produktnavn, Produktnummer, Antal, Mål, Producent, Produktkategori, Pris) VALUES (?, ?, ?, ?, ?, ?, ?)"
        data = (produktnavn, produktnummer, antal, mål, producent, produktkategori, pris)
        query2 = "SELECT ID, Produktnavn, Produktnummer, Antal, Mål, Producent, Produktkategori, Pris FROM Lageroversigt ORDER BY id ASC"

        try:
            cur = conn.cursor()
            cur.execute(query, data)
            conn.commit()
            cur.execute(query2)
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

        fjern_vare = request.form.get('fjern_vare')
        conn = sqlite3.connect(database='database/ny_database.db')
        query5 = f"DELETE FROM Lageroversigt WHERE id={fjern_vare}"
        query6 = "SELECT ID, Produktnavn, Produktnummer, Antal, Mål, Producent, Produktkategori, Pris FROM Lageroversigt ORDER BY id ASC"
        try:
            cur = conn.cursor()
            cur.execute(query5)
            conn.commit()
            cur.execute(query6)
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

        

        # Jacobs
        # produktnavn = request.form.get('produktnavn')
        # produktnummer = request.form.get('produktnummer')
        # antal = request.form.get('antal')
        # bredde = request.form.get('bredde')
        # bredde_enhed = request.form.get('bredde_enhed')
        # if bredde_enhed == "m":
        #     bredde = "%.2f" % float(bredde)
        # længde = request.form.get('længde')
        # længde_enhed = request.form.get('længde_enhed')
        # if længde_enhed == "m":
        #     længde = "%.2f" % float(længde)
        # mål = f"B: {bredde} {bredde_enhed} L: {længde} {længde_enhed}"
        # producent = request.form.get('producent')
        # produktkategori = request.form.get('produktkategori')
        # pris = request.form.get('pris')
        # produktinfo = [produktnavn, produktnummer, antal, mål, producent,produktkategori, pris]
        # print(produktinfo)
        
        # match(produktnavn, produktnummer, antal, mål, producent,produktkategori, pris)
        # Jacobs slut

    return render_template('lager.html', data_rows = data_rows)

@app.route('/bestilte_varer')
def bestilte_varer():
    return render_template('bestilte_varer.html')

@app.route('/prisliste')
def prisliste():
    return render_template('prisliste.html')


app.run(debug=True)