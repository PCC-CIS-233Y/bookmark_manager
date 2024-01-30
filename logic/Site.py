class Site:
    __url = ""
    __title = ""
    __description = ""
    __icon = None

    def __init__(self, url, title, description):
        self.__url = url
        self.__title = title
        self.__description = description

    def __str__(self):
        return f"{self.__title}: {self.__url}, {self.__description}"

    @staticmethod
    def read_bookmarks():
        from data.Database import Database

        return Database.read_bookmarks()
