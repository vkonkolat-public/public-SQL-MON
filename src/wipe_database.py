from sqlcenter import SQLCenter

# This file is used to wipe the database clean. It will just freaking delete everything. Use with care.
# Due to it's unnatural firepower it is not included anywhere yet.
# Migrated to use SQLcenter 2026-11-24, ketp to retain old run functionality

def wipe_database():
    SQLCenter().wipe_database()


if __name__ == "__main__":
    wipe_database()