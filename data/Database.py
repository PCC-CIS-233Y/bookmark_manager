from logic.Site import Site
from logic.RegisteredSite import RegisteredSite

class Database:
    @staticmethod
    def read_bookmarks():
        return [
            Site("https://www.google.com/", "Google Search", "Biggest search engine on the web."),
            RegisteredSite("https://www.pcc.edu/", "PCC Homepage", "My school", "marc.goodman", "???"),
            Site("https://www.imdb.com/", "Internet Movie Database", "All movies, TV series, etc."),
            RegisteredSite("https://bankofamerica.com/", "Bank of America", "My bank", "marc.goodman", "???"),
            Site("https://hurawatch.ru/", "Hurawatch", "Russia-located media pirate site")
        ]