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

    def __contains__(self, item):
        return item in self.__bookmarks

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def add(self, bookmark):
        self.__bookmarks.append(bookmark)

    def remove(self, bookmark):
        self.__bookmarks.remove(bookmark)

    def __add__(self, other):
        new_name = self.get_name() + "/" + other.get_name()
        try:
            new_category = Category.lookup(new_name)
            if new_category is not None:
                raise Exception(f"Error! Category {new_category.get_name()} already exists!")
        except KeyError:
            new_category = None
        description = self.get_description() + " and also " + other.get_description()
        # average = (self.get_level() + other.get_level()) / 2
        # average = max(self.get_level(), other.get_level())
        new_category = Category(new_name, description, [])
        for bookmark in self:
            if bookmark not in new_category:
                new_category.add(bookmark)
        for bookmark in other:
            if bookmark not in new_category:
                new_category.add(bookmark)
        return new_category

    @classmethod
    def lookup(cls, name):
        return cls.__map[name.lower()]

    @staticmethod
    def read_data():
        from data.Database import Database

        return Database.read_data()