class Site:
    url = ""
    title = ""
    description = ""
    icon = None

    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def __str__(self):
        return f"{self.title}: {self.url}, {self.description}"

    @staticmethod
    def read_bookmarks():
        from data.Database import Database

        return Database.read_bookmarks()
