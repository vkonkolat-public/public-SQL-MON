import sqlite3
from flask import g

def get_connection():
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

# Some trickery led to to the database getting locked via a connection that was left open and never dropped. No weaknesses!
# TODO: Closing the connection at the part where the raised exception is catched?
def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()

# Evil hack to bypass application context dependency
def vexecute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    con.close()

def last_insert_id():
    return g.last_insert_id    
    
# Mitä vittua tämä query varsinaisesti palauttaa rakenteeltaan? 
# Se on list of tuples, jossa jokainen tuple on rivi ja tuple sisältää sarakkeiden arvot. 
# Eli jos teet SELECT * FROM table, saat listan, jossa jokainen elementti on tuple, joka sisältää kaikki sarakkeet kyseiseltä riviltä.
# Uuuuh, kiitos herra AI mestari autofill
def query(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result