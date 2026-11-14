# TODO: Muistio aivoille: COnsider merging with db.py
import sqlite3
import db
import os.path

# Tries to create the database based on schema.sql
# TODO: add exception handling and shieet later
def create_database():
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    with open("schema.sql", "r") as f:
        con.executescript(f.read())
    con.close()

# Cheks if the database file exists. Returns True or false
# TODO: Currently checks the same folder, increase robustness with development 
def check_database_exists(location:str="database.db") -> bool:
    return os.path.exists(location)

# TODO: Doesn't at the moment check for right format, definitely add later
def main():
    #Check if the database already exists
    try:
        if check_database_exists():
            print("Database already exists.")
            return
    except Exception as e:
        print(f"Error checking database existence: {e}")
        return

    print("Database did not, in fact, exist.")
    #If database does not exist, create it
    create_database()
    print("Database created successfully.")


if __name__ == "__main__":
    main()
