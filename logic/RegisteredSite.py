from logic.Site import Site

class RegisteredSite(Site):
    __account = ""
    __password = ""

    def __init__(self, url, title, description, last_changed, account, password):
        super().__init__(url, title, description, last_changed)
        self.__account = account
        self.__password = password

    def __str__(self):
        return super().__str__() + f" {self.__account}:{self.__password}"

    def to_dict(self):
        dict = super().to_dict()
        dict["account"] = self.__account
        dict["password"] = self.__password
        dict["type"] = "RegisteredSite"
        return dict