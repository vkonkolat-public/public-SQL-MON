import db
from werkzeug.security import generate_password_hash, check_password_hash

# This script provides an alternative way to populate the database, python makes is way easier to run checks and insert massive
# amounts of randomised test data
def create_mikko():
    # Check if the user Mikko already exists
    result = db.query("SELECT * FROM users WHERE username = ?", ["Mikko"])
    if result:
        print("Database already populated (at this point with only Mikko)")
        mikko_id = db.query("SELECT id FROM users WHERE username = ?", ["Mikko"])[0]["id"]
        result = db.query("SELECT * FROM mons WHERE mon_name = ? AND user_id = ?", ["Pekka", mikko_id])
        if not result:
            print("Somehow, somehow Mikko exists but his SQL-MON Pekka doesn't. I thought future me would like to know this, t. past you")
        return

    # Creates user Mikko with password "4"
    # HOT TOPIC: At the moment of writing this, 15.11.2026, password being 4 instead of more traditional 42 or 69 is due to eMudhra
    # debacle where important 115-digit key was 4
    
    # hash the password
    password_hash = generate_password_hash("4")

    # Create the user in the database
    db.vexecute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ["Mikko", password_hash])
    mikko_id = db.query("SELECT id FROM users WHERE username = ?", ["Mikko"])[0]["id"]
    print(f"User Mikko created with ID: {mikko_id}")


    # Create a SQL-MON for Mikko with the following details: 
    # Name - Pekka, 
    # Vimma - 20, 
    # Sisu - 15, 
    # Kesto - 100
    db.vexecute("INSERT INTO mons (mon_name, vimma, sisu, kesto, user_id) VALUES (?, ?, ?, ?, ?)", ["Pekka", 20, 15, 100, mikko_id])

    # Check if the SQL-MON was created successfully and belongs to Mikko
    result = db.query("SELECT * FROM mons WHERE mon_name = ? AND user_id = ?", ["Pekka", mikko_id])

    if result:
        print("Database populated successfully with user Mikko and SQL-MON Pekka.")
    else:
        print("Något gick fel.")

if __name__ == "__main__":
    create_mikko()