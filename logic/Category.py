class Category:
    __name = ""
    __description = ""
    __bookmarks = []
    __map = {}
    ALL_BOOKMARKS = "All Bookmarks"

    def __init__(self, name, description, bookmarks):
        self.__name = name
        self.__description = description
        self.__bookmarks = bookmarks
        self.__class__.__map[name.lower()] = self

    def __str__(self):
        return f"<Category: {self.__name}>"

    def __iter__(self):
        return self.__bookmarks.__iter__()

    def get_name(self):
        return self.__name

    @classmethod
    def lookup(cls, name):
        return cls.__map[name.lower()]

    @staticmethod
    def read_data():
        from data.Database import Database

        return Database.read_data()