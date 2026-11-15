# CREATE TABLE mons (
#     id INTEGER PRIMARY KEY,
#     mon_name TEXT NOT NULL,
#     vimma INTEGER,
#     sisu INTEGER,
#     kesto INTEGER,
#     user_id INTEGER REFERENCES users
# );
# Class to handle fetching SQL MON data
import db
class SQLCenter:
    def __init__(self):
        self.db = db

    def get_user_data(self, user_id):
        return self.db.query("SELECT * FROM users WHERE id = ?", [user_id])

    def get_mon_data(self, mon_id):
        return self.db.query("SELECT * FROM mons WHERE id = ?", [mon_id])

    def get_all_mons_for_user(self, user_id):
        return self.db.query("SELECT * FROM mons WHERE user_id = ?", [user_id])

    def create_mon_for_user(self, user_id, mon_name, vimma, sisu, kesto):
        self.db.execute(
            "INSERT INTO mons (user_id, mon_name, vimma, sisu, kesto) VALUES (?, ?, ?, ?, ?)", [user_id, mon_name, vimma, sisu, kesto]
        )