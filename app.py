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
    conn = sqlite3.connect(database='database/database.db')
    QUERY = "SELECT Produktnavn, Produkttype, Produktnummer, Producent, Antal, Mål, Pris FROM Lager ORDER BY id DESC"

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
        produkttype = request.form.get('produkttype')
        produktnummer = request.form.get('produktnummer')
        producent = request.form.get('producent')
        antal = request.form.get('antal')
        mål = request.form.get('mål')
        pris = request.form.get('pris')
       
        conn = sqlite3.connect(database='database/database.db')
        query = "INSERT INTO Lager(Produktnavn, Produkttype, Produktnummer, Producent, Antal, Mål, Pris) VALUES (?, ?, ?, ?, ?, ?, ?)"
        data = (produktnavn, produkttype, produktnummer, producent, antal, mål, pris)
        query2 = "SELECT Produktnavn, Produkttype, Produktnummer, Producent, Antal, Mål, Pris FROM Lager ORDER BY id DESC"

        try:
            cur = conn.cursor()
            cur.execute(query, data)
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