from werkzeug.security import check_password_hash, generate_password_hash

from sqlcenter import DuplicateUsernameError


class DuplicateUserError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class UnknownUserError(InvalidCredentialsError):
    pass


class InvalidPasswordError(InvalidCredentialsError):
    pass


class InvalidMonError(Exception):
    pass


# Services keep application rules separate from SQLCenter's database operations.
class UserService:
    def __init__(self, sqlcenter):
        self.sqlcenter = sqlcenter

    def authenticate(self, username, password):
        rows = self.sqlcenter.get_user_by_username(username)
        if not rows:
            raise UnknownUserError

        user_id, password_hash = rows[0]
        if not check_password_hash(password_hash, password):
            raise InvalidPasswordError

        return user_id

    def register(self, username, password1, password2):
        if password1 != password2:
            raise InvalidCredentialsError

        password_hash = generate_password_hash(password1)
        try:
            self.sqlcenter.create_user(username, password_hash)
        # This is.... what? Why does the error class change?
        except DuplicateUsernameError as error:
            raise DuplicateUserError from error


class SQLMonService:
    # TODO: Move SQLMON statline to a separate class and build everything reliant on the stats from that source.
    ALLOWED_STATS = {
        "vimma": "vimma",
        "sisu": "sisu",
        "kesto": "kesto",
    }

    def __init__(self, sqlcenter):
        self.sqlcenter = sqlcenter

    def record_visit(self):
        self.sqlcenter.record_visit()
        rows = self.sqlcenter.get_visit_count()
        # Row factory makes it possible to use names instead of indexes:
        # return int(rows[0]["count"]) if rows else 0
        return int(rows[0][0]) if rows else 0

    def get_for_user(self, user_id):
        return self.sqlcenter.get_all_mons_for_user(user_id)

    def increase_stat(self, mon_id, user_id, stat):
        column = self.ALLOWED_STATS.get(stat)
        if column is None:
            raise InvalidMonError
        if not self.sqlcenter.owns_mon(mon_id, user_id):
            raise InvalidMonError
        self.sqlcenter.increase_mon_stat(mon_id, user_id, column)

    # TODO: Create what? A mon for certain user. Look into this later. Definitely name better
    def create(self, user_id, mon_name, vimma, sisu, kesto):
        if not mon_name or any(value < 0 for value in (vimma, sisu, kesto)):
            raise InvalidMonError
        self.sqlcenter.create_mon_for_user(user_id, mon_name, vimma, sisu, kesto)
