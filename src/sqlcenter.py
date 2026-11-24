# Sisäänrakennetut kirjastot
import sqlite3
from pathlib import Path

# Omat importit
import db

# This class exists solely to give a unique message in a specific case, it certainly goes around
class DuplicateUsernameError(Exception):
    pass


# Muistio aivoille: Arvot laitettiin kysymysmerkin kautta. Nyt ne parametrisoidaan pakollisesti jottei joku "ilkeä hacker" korvaa hakuehtoa arvolla "whoCares OR 42==42 [kommentoi loput]"
# Jolloin saadaan tyhmistä kyselyistä ulos vaikka SELECT * FROM users WHERE 42==42 [aina totta];
class SQLCenter:
    def __init__(self):
        self.db = db

    # User data operations
    def get_user_data(self, user_id):
        return self.db.query("SELECT * FROM users WHERE id = ?", [user_id])

    def get_user_by_username(self, username):
        return self.db.query(
            "SELECT id, password_hash FROM users WHERE username = ?",
            [username],
        )

    def create_user(self, username, password_hash):
        try:
            self.db.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                [username, password_hash],
            )
        except sqlite3.IntegrityError as error:
            raise DuplicateUsernameError from error

    # Record relic, definitely keeping on the front page.
    def record_visit(self):
        self.db.execute(
            "INSERT INTO visit_counter (visited_at) VALUES (datetime('now'))"
        )

    def get_visit_count(self):
        return self.db.query("SELECT COUNT(*) FROM visit_counter")

    # Mon data operations
    def get_mon_data(self, mon_id):
        return self.db.query("SELECT * FROM mons WHERE id = ?", [mon_id])

    def get_mon_by_name_and_user(self, mon_name, user_id):
        return self.db.query(
            "SELECT * FROM mons WHERE mon_name = ? AND user_id = ?",
            [mon_name, user_id],
        )

    def get_all_mons_for_user(self, user_id):
        return self.db.query("SELECT * FROM mons WHERE user_id = ?", [user_id])

    def owns_mon(self, mon_id, user_id):
        result = self.db.query(
            "SELECT id FROM mons WHERE id = ? AND user_id = ?",
            [mon_id, user_id],
        )
        return bool(result)

    # This is currently increasing by one and exposes some vulnerabilities if the mon doesn't exist
    # Rework later for balnances and such
    def increase_mon_stat(self, mon_id, user_id, stat_column):
        self.db.execute(
            f"UPDATE mons SET {stat_column} = COALESCE({stat_column}, 0) + 1 "
            "WHERE id = ? AND user_id = ?",
            [mon_id, user_id],
        )

    # TODO: Definitely abstract these default stats/fields somehwere
    def create_mon_for_user(self, user_id, mon_name, vimma, sisu, kesto):
        self.db.execute(
            "INSERT INTO mons (user_id, mon_name, vimma, sisu, kesto) "
            "VALUES (?, ?, ?, ?, ?)",
            [user_id, mon_name, vimma, sisu, kesto],
        )

    # Be pretty fucking careful with this one, remember to make extra prompt page for any html page referring to his
    # Sensitive operation. Yeah. The user shouldn't be allowed to call this under any circumstances outside testing or debug mode. 
    def wipe_database(self):
        for sql in (
            "DELETE FROM fights",
            "DELETE FROM past_combatants",
            "DELETE FROM mons",
            "DELETE FROM users",
            "DELETE FROM visit_counter",
        ):
            self.db.vexecute(sql)

    # TODO: replace this schizobabble with bachelor level code solution later. I don't need path resolving and encoding setting to reading a sqlite database from the same directory.
    def create_schema(self):
        con = self.db.get_connection()
        try:
            schema_path = Path(__file__).resolve().parent / "schema.sql"
            con.executescript(schema_path.read_text(encoding="utf-8"))
        finally:
            con.close()
