class Site:
    __url = ""
    __title = ""
    __description = ""
    __icon = None
    __map = {}

    def __init__(self, url, title, description):
        self.__url = url
        self.__title = title
        self.__description = description
        Site.__map[url.lower()] = self

    def __str__(self):
        return f"{self.__title}: {self.__url}, {self.__description}"

    @classmethod
    def lookup(cls, url):
        return cls.__map[url.lower()]
