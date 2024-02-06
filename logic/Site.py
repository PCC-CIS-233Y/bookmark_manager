from datetime import datetime

class Site:
    __url = ""
    __title = ""
    __description = ""
    __last_changed = ""
    __icon = None
    __map = {}

    def __init__(self, url, title, description, last_changed):
        self.__url = url
        self.__title = title
        self.__description = description
        self.__last_changed = last_changed
        Site.__map[url.lower()] = self

    def get_url(self):
        return self.__url

    def set_description(self, description):
        self.__description = description
        self.__last_changed = str(datetime.now())

    def __str__(self):
        return f"{self.__title}: {self.__url}, {self.__description}, last changed: {self.__last_changed}"

    @classmethod
    def lookup(cls, url):
        return cls.__map[url.lower()]
