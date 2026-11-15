import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash # No need to get fancy with thsese
import config

import db
import sqlcenter

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

@app.route("/404")
def not_found():
    return render_template("404.html"), 404

@app.errorhandler(404)
def handle_not_found(error):
    return redirect(url_for("not_found"))

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    # Fetch the password hash for the given username and handle errors if the user does not exist
    sql = "SELECT password_hash FROM users WHERE username = ?"
    try:
        password_hash = db.query(sql, [username])[0][0]
    except (IndexError, TypeError) as e:
        print(f"Error fetching password hash: {e}")
        return "VIRHE: käyttäjää ei löydy"

    # Check if the provided password matches the stored hash an boot them off if it doesn't
    if check_password_hash(password_hash, password):
        session["username"] = username
        session["user_id"] = db.query("SELECT id FROM users WHERE username = ?", [username])[0][0]
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
    sqlcenter_instance = sqlcenter.SQLCenter()
    users_mons = sqlcenter_instance.get_all_mons_for_user(session["user_id"])
    return render_template("frontpage.html", mons=users_mons)

#TODO: This is a not fully understood method for a single page, make usable in a larger scope later
#TODO: Add a more descriptive way to fail than abort(404)
@app.post("/mons/<int:mon_id>/increase/<stat>")
def increase_mon_stat(mon_id, stat):
    if "user_id" not in session:
        return redirect("/")

    stat_columns = {
        "vimma": "vimma",
        "sisu": "sisu",
        "kesto": "kesto",
    }
    column = stat_columns.get(stat)
    if column is None:
        abort(404)

    mon = db.query(
        "SELECT id FROM mons WHERE id = ? AND user_id = ?",
        [mon_id, session["user_id"]],
    )
    if not mon:
        abort(404)

    db.execute(
        f"UPDATE mons SET {column} = COALESCE({column}, 0) + 1 WHERE id = ? AND user_id = ?",
        [mon_id, session["user_id"]],
    )
    return redirect(url_for("frontpage"))

#Simple redirect back to the lander page
# How does this handle multiple sessions?
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/SQLMON_creation")
def SQLMON_creation():
    if "username" not in session:
        return redirect("/")
    return render_template("SQLMON_creation.html")

@app.route("/create_mon", methods=["POST"])
def create_mon():
    if "username" not in session:
        return redirect("/")
    sqlcenter_instance = sqlcenter.SQLCenter()
    sqlcenter_instance.create_mon_for_user(
        session["user_id"],
        request.form["mon_name"],
        int(request.form["vimma"]),
        int(request.form["sisu"]),
        int(request.form["kesto"])
    )
    return redirect("/frontpage")