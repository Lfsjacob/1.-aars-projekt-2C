import sqlite3


conn = sqlite3.connect(database='database/database.db')

query = "SELECT * FROM Lager"

try:
    cur = conn.cursor()
    cur.execute(query)
    # conn.commit()

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

for item in data_rows:
    for item in item:
        print(item)