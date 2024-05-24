from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Opretter en flask applikation
app = Flask(__name__)

# fortæller hvilken database flask-sqlalchemy skal forbinde
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://db.sqlite"
# Skriv en secret key
app.config["SECRET_KEY"] = "ENTER YOUR SECRET KEY"
# Opretter en instans af SQLAlchemy
db = SQLAlchemy(app)

# LoginManager skal bruges til app'en for at kunne logge ind og ud
login_manager = LoginManager()
login_manager.init_app(app)

# opretter en bruger model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brugernavn = db.Column(db.String(250), unique=True,
                         nullable=False)
    password = db.Column(db.String(250), 
                         nullable=False)

# intiere app med extension
db.init_app(app)
# Opretter en database indenfor app context
with app.app_context():
    db.create_all()
    
# opretter en bruger indlæsnings callback der returnerer det object der får et id
@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=["GET", "POST"])
def registrer():
    # hvis brugeren har lavet POST request, lav en ny bruger
    if request.method == "POST":
        user = Users(brugernavn=request.form.get("brugernavn"),
                     password=request.form.get("password"))
        # tilføj bruger til database
        db.session.add(user)
        # commit'er ændringer
        db.session.commit()
        # når bruger account er oprettet bliver man redirected til login route (som bliver lavet senere)
        return redirect(url_for("login"))
    # indlæser sign_up template hvis brugeren laver et GET request
    return render_template("sign_up.html")

# Opretter en login route 
@app.route('/login', methods=["GET", "POST"])
def login():
    # hvis der er lavet et POST request, find brugeren ved at filtrere efter brugernavn
    if request.method == "POST":
        user = User.query.filter_by(
            brugernavn=request.form.get("brugernavn")).first()
        # tjek om password stemmer overens med brugerens password
        if user and user.password == request.form.get("password"):
            # Brug login_user metoden til at bruger-login
            login_user(user)
            return redirect(url_for("home"))
        # Redirect the user back til 'home' 
return render_template("login.html")
    






