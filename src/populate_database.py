from werkzeug.security import generate_password_hash
import sqlcenter

# This script provides an alternative way to populate the database, python makes is way easier to run checks and insert massive
# amounts of randomised test data
def create_mikko():
    center = sqlcenter.SQLCenter()
    # Check if the user Mikko already exists
    result = center.get_user_by_username("Mikko")
    if result:
        print("Database already populated (at this point with only Mikko)")
        mikko_id = result[0]["id"]
        result = center.get_mon_by_name_and_user("Pekka", mikko_id)
        if not result:
            print("Somehow, somehow Mikko exists but his SQL-MON Pekka doesn't. I thought future me would like to know this, t. past you")
        return

    # Creates user Mikko with password "4"
    # HOT TOPIC: At the moment of writing this, 15.11.2026, password being 4 instead of more traditional 42 or 69 is due to eMudhra
    # debacle where important 115-digit key was 4
    
    # hash the password
    password_hash = generate_password_hash("4")

    # Create the user in the database
    center.create_user("Mikko", password_hash)
    mikko_id = center.get_user_by_username("Mikko")[0]["id"]
    print(f"User Mikko created with ID: {mikko_id}")

    # Create a SQL-MON for Mikko with the following details: 
    # Name - Pekka, 
    # Vimma - 20, 
    # Sisu - 15, 
    # Kesto - 100
    center.create_mon_for_user(mikko_id, "Pekka", 20, 15, 100)

    # Check if the SQL-MON was created successfully and belongs to Mikko
    result = center.get_mon_by_name_and_user("Pekka", mikko_id)

    if result:
        print("Database populated successfully with user Mikko and SQL-MON Pekka.")
    else:
        print("Något gick fel.")

# Untested, unchecked, look through before integrating to anything
# def create_random_users(num_users):
#     center = sqlcenter.SQLCenter()
#     for i in range(num_users):
#         username = f"user_{i}"
#         password_hash = generate_password_hash(f"password_{i}")
#         try:
#             center.create_user(username, password_hash)
#             print(f"User {username} created successfully.")
#         except sqlcenter.DuplicateUsernameError:
#             print(f"User {username} already exists. Skipping.")

if __name__ == "__main__":
    create_mikko()