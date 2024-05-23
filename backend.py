import sqlite3
from flask import request


def get_variables():
    x = request.form.get('første_variabel')
    return x














conn = sqlite3.connect(database='database.db')

try:
    cur = conn.cursor()
    cur.execute("")

except sqlite3.OperationalError as oe:
    print(f"Transaction could not be processed: {oe}")

except sqlite3.IntegrityError as ie:
    print(f"Integrity constraint violated: {ie}")

except sqlite3.ProgrammingError as pe:
    print(f"You used the wrong SQL table: {pe}")

except sqlite3.Error as e:
    print(f"Error calling SQL: {e}")

finally:
    conn.close()

