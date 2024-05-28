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

















# <h2>Tilføj vare:</h2>
#     <form action="" method="POST">
#         <label for="produktnavn">Produktnavn</label><br>
#         <input type="text" id="produktnavn" name="produktnavn"><br>
#         <br>

#         <label for="produktnummer">Produktnummer</label><br>
#         <input type="text" id="produktnummer" name="produktnummer"><br>
#         <br>

#         <label for="antal">Antal</label><br>
#         <input type="text" id="antal" name="antal"><br>
#         <br>

#         <label for="længde">Længde</label><br>
#         <input type="text" id="længde" name="længde"><br>
#         <br>

#         <label for="længde_enhed">Længdeenhed</label><br>
#         <input type="text" id="længde_enhed" name="længde_enhed"><br>
#         <br>

#         <label for="bredde">Bredde</label><br>
#         <input type="text" id="bredde" name="bredde"><br>
#         <br>

#         <label for="bredde_enhed">Bredde enhed</label><br>
#         <input type="text" id="bredde_enhed" name="bredde_enhed"><br>
#         <br>

#         <label for="mål">Mål</label><br>
#         <input type="text" id="mål" name="mål"><br>
#         <br>

#         <label for="producent">Producent</label><br>
#         <input type="text" id="producent" name="producent"><br>
#         <br>

#         <label for="produktkategori">Produktkategori</label><br>
#         <input type="text" id="produktkategori" name="produktkategori"><br>
#         <br>

#         <label for="pris">Pris</label><br>
#         <input type="text" id="pris" name="pris"><br>
#         <br>
#         <input type="submit" value="Submit">
#     </form>













# Nyeste

# <table>
#         <tr>
#             <th></th>
#             <th>Produktnavn</th>
#             <th>Produktnummer</th>
#             <th>Antal</th>
#             <th>Mål</th>
#             <th>Producent</th>
#             <th>Produktkategori</th>
#             <th>Pris</th>
#         </tr>

#         {% for item in data_rows %}
#         <tr>
#             <td><form action="" method="POST"><input type="submit" value="Fjern vare"></form></td>
#             {% for i in item %}
#             <td>{{ i }}</td>
#             {% endfor %}
#         </tr>
#         {% endfor%}
#     </table><br>
#     <br>








# <table>
#         <tr>
#             <th></th>
#             <th>Produktnavn</th>
#             <th>Produktnummer</th>
#             <th>Antal</th>
#             <th>Mål</th>
#             <th>Producent</th>
#             <th>Produktkategori</th>
#             <th>Pris</th>
#         </tr>

#         {% for item in data_rows %}
#         <tr>
#             {% for i in range(data_rows|length) %}
#             <td><form action="" method="POST"><input type="submit" value="bob"></form></td>
#             {% for item in item %}
#             <td>{{ item }}</td>
#             {% endfor %}
#         </tr>
#         {% endfor%}
#     </table><br>
#     <br>





# Det nyeste
# <table>
#         <tr>
#             <th></th>
#             <th>Produktnavn</th>
#             <th>Produktnummer</th>
#             <th>Antal</th>
#             <th>Mål</th>
#             <th>Producent</th>
#             <th>Produktkategori</th>
#             <th>Pris</th>
#         </tr>

#         {% for i in range(data_rows|length) %}
#         <tr>
#             <td><form action="" method="POST"><input type="submit" name="fjern_vare" value="{{ i }}"></form></td>
#             {% for item in data_rows[i] %}
#             <td>{{ item }}</td>
#             {% endfor %}
#         </tr>
#         {% endfor%}
#     </table>    








# <table>
#         <tr>
#             <th></th>
#             <th>ID</th>
#             <th>Produktnavn</th>
#             <th>Produktnummer</th>
#             <th>Antal</th>
#             <th>Mål</th>
#             <th>Producent</th>
#             <th>Produktkategori</th>
#             <th>Pris</th>
#         </tr>

#         {% for i in range(data_rows|length) %}
#         <tr>
#             <td><form action="" method="POST"><input type="submit" name="fjern_vare" value=""></form></td>
#             {% for item in data_rows[i] %}
#             <td>{{ item }}</td>
#             {% endfor %}
#         </tr>
#         {% endfor%}
#     </table> 
