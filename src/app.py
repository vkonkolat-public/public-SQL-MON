import sqlite3
from flask import Flask
from flask import redirect, render_template, request, url_for, session
import db
from werkzeug.security import generate_password_hash, check_password_hash # No need to get fancy with thsese
import config

app = Flask(__name__)
app.secret_key = config.secret_key

# @app.route("/")
# def index():
#     db.execute("INSERT INTO visit_counter (visited_at) VALUES (strftime('%s', 'now'))")
#     result = db.execute("SELECT COUNT(*) FROM visit_counter").fetchone()
#     count = result[0] if result else 0
#     return render_template("lander.html", visit_count=count)

@app.route("/")
def index():
    db.execute("INSERT INTO visit_counter (visited_at) VALUES (datetime('now'))")
    result = db.query("SELECT COUNT(*) FROM visit_counter") #Query instead?
    if result:
        count = result[0][0]
        try:
            count = int(count)
        except (ValueError, TypeError) as e:
            count = 0
            print(f"Error converting count to int: {e}, något gick fel. {count}")
    else: 
        count = 0
        print("No result from query, setting count to 0.")
        # TODO: Link these to actual testing instead of bum rushing

    return render_template("lander.html", visit_count=count)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    sql = "SELECT password_hash FROM users WHERE username = ?"
    password_hash = db.query(sql, [username])[0][0]

    if check_password_hash(password_hash, password):
        session["username"] = username
        return redirect("/frontpage")
    else:
        return "VIRHE: väärä tunnus tai salasana"

@app.route("/registration")
def registration():
    return render_template("registration.html")


#TODO: Find out a way to make this a proper page with proper logic, get done away with sqlite3 and use the cool style for html
@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return render_template("creation_attempt.html", message="VIRHE: salasanat eivät ole samat")
        
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return render_template("creation_attempt.html", message="VIRHE: tunnus on jo varattu")
        #TODO: BIG BRAIN MOMENT: This exception seems to leave an open connection to the database. 

    return render_template("creation_attempt_succesful.html", message="Tunnus luotu.")

# This should be the frontpage for logged in users, set aside from the lander page
@app.route("/frontpage")
def frontpage():
    if "username" not in session:
        return redirect("/")
    return render_template("frontpage.html")

#Simple redirect back to the lander page
# How does this handle multiple sessions?
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")