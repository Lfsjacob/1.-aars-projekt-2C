import sqlite3
from flask import Flask, render_template, request, url_for, redirect

master_key = "magickey"

app = Flask(__name__)
app.config["SECRET_KEY"] = "abc"


@app.route('/register', methods=["GET", "POST"])
def register():
	global master_key
	received_key = request.form.get('master_password')
	if request.method == "POST" and received_key == master_key:
		username = request.form.get('brugernavn')
		password = request.form.get('password')
		print(f"{username = }")
		print(f"{password = }  ")
		try:
			conn = sqlite3.connect(database="instance/adminbrugere.db")
			cur = conn.cursor()
			query = f"INSERT INTO users(username, password) VALUES(?, ?)"
			data = (username, password)
			cur.execute(query, data)
			conn.commit()
		except sqlite3.Error as e:
			conn.rollback()
			print(f"Kunne ikke oprette {e}")

	

	return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		username = request.form.get('brugernavn')
		password = request.form.get('password')
		conn= sqlite3.connect(database="instance/adminbrugere.db")
		cur = conn.cursor()
		query = f"SELECT * FROM users"
		data = (username, password)
		cur.execute(query, data)
		for row in cur:
			if row[0] == username and row[1] == password:
				return redirect("/home", code=302)

	return render_template("login.html")



@app.route("/")
def hjem():
	return render_template("login.html")

@app.route("/home")
def home():
	return render_template("home.html")

if __name__ == "__main__":
	app.run()