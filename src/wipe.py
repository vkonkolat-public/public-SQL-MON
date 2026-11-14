import db

# This file is used to wipe the database clean. It will just freaking delete everything. Use with care.
# Due to it's unnatural firepower it is not included anywhere yet.

db.execute("DELETE FROM users")
db.execute("DELETE FROM mons")
db.execute("DELETE FROM past_combatants")
db.execute("DELETE FROM fights")
db.execute("DELETE FROM visits")