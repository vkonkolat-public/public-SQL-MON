from flask import Flask
from flask import abort, redirect, render_template, request, url_for, session

import config
import sqlcenter
from services import (
    DuplicateUserError,
    InvalidCredentialsError,
    InvalidMonError,
    InvalidPasswordError,
    SQLMonService,
    UserService,
    UnknownUserError,
)



app = Flask(__name__)
# secret_key = "00000000000000000000000000000004"
# Toivottavasti kukaan 'evil hacker' ei löydä tätä varhaisesta github commitista. Saar niiden kaiveleminen on kiellettyä.
app.secret_key = config.secret_key
sql_center = sqlcenter.SQLCenter()
user_service = UserService(sql_center)
mon_service = SQLMonService(sql_center)



@app.route("/")
def index():
    count = mon_service.record_visit()
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

    try:
        user_id = user_service.authenticate(username, password)
    except UnknownUserError:
        return "VIRHE: käyttäjää ei löydy"
    except InvalidPasswordError:
        return "VIRHE: väärä tunnus tai salasana"

    session["username"] = username
    session["user_id"] = user_id
    return redirect("/frontpage")

@app.route("/registration")
def registration():
    return render_template("registration.html")

# Route for creating a new user.
# TODO: Check error categories and handling for: existing username, password mismatch, invalid characters, etc. 
@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    try:
        user_service.register(username, password1, password2)
    except InvalidCredentialsError:
        return render_template(
            "creation_attempt.html",
            message="VIRHE: salasanat eivät ole samat",
        )
    except DuplicateUserError:
        return render_template("creation_attempt.html", message="VIRHE: tunnus on jo varattu")
    return render_template("creation_attempt_succesful.html", message="Tunnus luotu.")

# This should be the frontpage for logged in users, set aside from the lander page
# TODO: Do some magic with teh layout.html tech unlocked earlier. Login/Register/Logout button at one corner and the usual stuff at one side in a colum behind { % if "username" in session % } cajonescaca
@app.route("/frontpage")
def frontpage():
    if "username" not in session:
        return redirect("/")
    users_mons = mon_service.get_for_user(session["user_id"])
    return render_template("frontpage.html", mons=users_mons)

#TODO: Add a more descriptive way to fail than abort(404)
@app.post("/mons/<int:mon_id>/increase/<stat>")
def increase_mon_stat(mon_id, stat):
    if "user_id" not in session:
        return redirect("/")

    try:
        mon_service.increase_stat(mon_id, session["user_id"], stat)
    except InvalidMonError:
        abort(404)
    return redirect(url_for("frontpage"))

#Simple redirect back to the lander page
# How does this handle multiple sessions?
@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    return redirect("/")

# Think about how to prevent users from creating crisscrossing mons or faking each other later. CUrrent
@app.route("/SQLMON_creation")
def SQLMON_creation():
    if "username" not in session:
        return redirect("/")
    return render_template("SQLMON_creation.html")

@app.route("/create_mon", methods=["POST"])
def create_mon():
    if "username" not in session:
        return redirect("/")
    try:
        mon_service.create(
            session["user_id"],
            request.form["mon_name"],
            int(request.form["vimma"]),
            int(request.form["sisu"]),
            int(request.form["kesto"]),
        )
    except (ValueError, InvalidMonError):
        abort(404)
    return redirect("/frontpage")