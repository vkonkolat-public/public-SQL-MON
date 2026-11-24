import os.path

import db
from sqlcenter import SQLCenter


def create_database():
    SQLCenter().create_schema()

def check_database_exists(location: str = db.DATABASE_PATH) -> bool:
    return os.path.exists(location)

def main():
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
