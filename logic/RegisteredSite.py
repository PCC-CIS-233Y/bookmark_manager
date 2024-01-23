from logic.Site import Site

class RegisteredSite(Site):
    account = ""
    password = ""

    def __init__(self, url, title, description, account, password):
        super().__init__(url, title, description)
        self.account = account
        self.password = password

    def __str__(self):
        return super().__str__() + f" {self.account}:{self.password}"