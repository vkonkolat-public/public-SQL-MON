import db

# This file is used to wipe the database clean. It will just freaking delete everything. Use with care.
# Due to it's unnatural firepower it is not included anywhere yet.

def wipe_database():
    # Delete child rows before parent rows because foreign keys are enabled.
    db.vexecute("DELETE FROM fights")
    db.vexecute("DELETE FROM past_combatants")
    db.vexecute("DELETE FROM mons")
    db.vexecute("DELETE FROM users")
    db.vexecute("DELETE FROM visit_counter")


if __name__ == "__main__":
    wipe_database()