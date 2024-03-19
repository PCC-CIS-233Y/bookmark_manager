import bcrypt

class User:
    __username = ""
    __password_hash = ""

    def __init__(self, username, password_hash):
        self.__username = username
        self.__password_hash = password_hash

    def verify_user(self, password):
        # return true if password matches stored hash and false otherwise.
        return bcrypt.checkpw(password.encode(), self.__password_hash)

    def get_key(self):
        return self.__username.lower()

    def get_username(self):
        return self.__username

    def to_dict(self):
        return {
            "_id": self.get_key(),
            "username": self.__username,
            "password_hash": self.__password_hash
        }

    @classmethod
    def build(cls, dict):
        if dict is None:
            return None
        return User(dict["username"], dict["password_hash"])

    @classmethod
    def read_user(cls, username):
        from data.Database import Database

        return Database.read_user(username)