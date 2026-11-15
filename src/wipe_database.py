import db

# This file is used to wipe the database clean. It will just freaking delete everything. Use with care.
# Due to it's unnatural firepower it is not included anywhere yet.

db.vexecute("DELETE FROM users")
db.vexecute("DELETE FROM mons")
db.vexecute("DELETE FROM past_combatants")
db.vexecute("DELETE FROM fights")
db.vexecute("DELETE FROM visit_counter")