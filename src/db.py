import sqlite3
from pathlib import Path

# TODO: Jos ajetaan pytestejä ajetaan testidb:ssä, muuten käytetään production db:tä, katso myöhemmin miten hoidetaan, toistaiseksi DATABASE_PATH saa olla ihman if/else branchia. Kyllä haluan toteuttaa jonkun ifTestEnvironment jutun
DATABASE_PATH = Path(__file__).resolve().parent / "database.db"


# This can be used to set the database path for testing purposes, so that tests don't interfere with the production database.
def configure_database_path(path):
    global DATABASE_PATH
    DATABASE_PATH = Path(path).resolve()

# Bread and butter connection function
def get_connection():
    con = sqlite3.connect(DATABASE_PATH)
    con.execute("PRAGMA foreign_keys = ON")
    # row_factory allows you to use row["column_name"] instead of row[0], which is much more readable and easier to read that [bumrush][0][1][0]
    con.row_factory = sqlite3.Row
    return con

# This should fix the hanging open connection in some cases, keep an eye out for perverse behaviour.
def execute(sql, params=None):
    con = get_connection()
    try:
        result = con.execute(sql, params or [])
        con.commit()
        return result.lastrowid
    finally:
        con.close()

# This is currently mostly obsolete, make something funky happen later
def vexecute(sql, params=None):
    return execute(sql, params)

# I hope the try/finally block hardens this enough against failing queries.
def query(sql, params=None):
    con = get_connection()
    try:
        return con.execute(sql, params or []).fetchall()
    finally:
        con.close()
