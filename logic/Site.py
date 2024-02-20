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
        Site.__map[self.get_key()] = self

    @classmethod
    def build(cls, dict):
        from logic.RegisteredSite import RegisteredSite

        if dict["type"] == "Site":
            return Site(dict["url"], dict["title"], dict["description"], dict["last_changed"])
        elif dict["type"] == "RegisteredSite":
            return RegisteredSite(dict["url"], dict["title"], dict["description"], dict["last_changed"],
                                  dict["account"], dict["password"])
        else:
            raise Exception(f"Unknown site type: {dict['type']}!")

    def get_key(self):
        return self.__url.lower()

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

    def to_dict(self):
        return {
            "_id": self.get_key(),
            "type": "Site",
            "url": self.__url,
            "title": self.__title,
            "description": self.__description,
            "last_changed": self.__last_changed
        }

    def add_to_database(self):
        from data.Database import Database

        Database.add_bookmark(self)