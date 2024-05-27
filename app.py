from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)

# Functions


# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lager', methods = ['POST', 'GET'])
def lager():
    data_rows = []
    conn = sqlite3.connect(database='database/ny_database.db')
    QUERY = "SELECT Produktnavn, Produktnummer, Antal, Mål, Producent, Produktkategori, Pris FROM Lageroversigt ORDER BY id DESC"

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
        query2 = "SELECT Produktnavn, Produktnummer, Antal, Mål, Producent, Produktkategori, Pris FROM Lageroversigt ORDER BY id DESC"

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

        

    return render_template('lager.html', data_rows = data_rows)

@app.route('/bestilte_varer')
def bestilte_varer():
    return render_template('bestilte_varer.html')

@app.route('/prisliste')
def prisliste():
    return render_template('prisliste.html')


app.run(debug=True)