from logic.Site import Site
from logic.RegisteredSite import RegisteredSite
from logic.Category import Category
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class Database:
    __client = None
    __bookmarks_collection = None
    __categories_collection = None

    @classmethod
    def connect(cls):
        if cls.__client is None:
            uri = "mongodb+srv://showuser:showuser@shows.gv7nqze.mongodb.net/?retryWrites=true&w=majority"
            # Create a new client and connect to the server
            client = MongoClient(uri, server_api=ServerApi('1'))
            cls.__bookmarks_database = client.Bookmarks
            cls.__bookmarks_collection = cls.__bookmarks_database.Bookmarks
            cls.__categories_collection = cls.__bookmarks_database.Categories
            # print(client)
            # print(cls.__bookmarks_database)
            # print(cls.__bookmarks_collection)
            # print(cls.__categories_collection)

    @classmethod
    def read_categories(cls):
        cls.connect()
        category_dicts = list(cls.__categories_collection.find())
        # for category_dict in category_dicts:
        #     print(category_dict)
        category_objects = [Category.build(category_dict) for category_dict in category_dicts]
        # for category_object in category_objects:
        #     print(category_object.get_name())
        #     for bookmark_object in category_object:
        #         print("    " + str(bookmark_object))
        return Category.lookup(Category.ALL_BOOKMARKS), category_objects

    @classmethod
    def read_bookmarks(cls):
        cls.connect()
        bookmark_dicts = list(cls.__bookmarks_collection.find())
        # for bookmark_dict in bookmark_dicts:
        #     print(bookmark_dict)
        bookmark_objects = [Site.build(bookmark_dict) for bookmark_dict in bookmark_dicts]
        # for bookmark_object in bookmark_objects:
        #     print(bookmark_object)

    @classmethod
    def close_connection(cls):
        cls.__client.close()

    @classmethod
    def rebuild_data(cls):
        cls.connect()
        cls.__categories_collection.drop()
        cls.__categories_collection = cls.__bookmarks_database.Categories
        cls.__bookmarks_collection.drop()
        cls.__bookmarks_collection = cls.__bookmarks_database.Bookmarks

        all_bookmarks, all_categories = cls.build_dummy_data()
        category_dicts = [category.to_dict() for category in all_categories]
        # for category in all_categories:
        #     print(category)
        cls.__categories_collection.insert_many(category_dicts)

        bookmark_dicts = [bookmark.to_dict() for bookmark in all_bookmarks]
        # for bookmark in bookmark_dicts:
        #     print(bookmark)
        cls.__bookmarks_collection.insert_many(bookmark_dicts)

    @classmethod
    def read_data(cls):
        cls.read_bookmarks()
        all_bookmarks_category, list_of_all_categories = cls.read_categories()
        return all_bookmarks_category, list_of_all_categories

    @staticmethod
    def build_dummy_data():
        google = Site("https://www.google.com/", "Google Search", "Biggest search engine on the web.", str(datetime.now()))
        bing = Site("https://www.bing.com/", "Bing Search", "Search engine from MicroSoft. Now with AI.", str(datetime.now()))
        pcc = RegisteredSite("https://www.pcc.edu/", "PCC Homepage", "My school", str(datetime.now()), "marc.goodman", "???")
        imdb = Site("https://www.IMDB.com/", "Internet Movie Database", "All movies, TV series, etc.", str(datetime.now()))
        boa = RegisteredSite("https://bankofamerica.com/", "Bank of America", "My bank", str(datetime.now()), "marc.goodman", "???")
        chase = Site("https://www.chase.com/", "Chase bank", "My wife's bank", str(datetime.now()))
        hurawatch = Site("https://hurawatch.ru/", "Hurawatch", "Russia-located media pirate site", str(datetime.now()))
        youtube = RegisteredSite("https://youtube.com/", "YouTube", "Video sharing site.", str(datetime.now()), "Marc", "???")

        search = Category("Search Engines", "Places where you can find links.", [google, bing])
        school = Category("School", "Sites related to school.", [pcc])
        finance = Category("Finance", "Finance sites.", [boa, chase])
        entertainment = Category("Entertainment", "Entertainment Sites", [imdb, hurawatch])
        video_streaming = Category("Video Streaming", "Video streaming sites.", [hurawatch, youtube])
        all_bookmarks = Category(Category.ALL_BOOKMARKS, "All the bookmarks known to the system. Automatically updated.", [google, bing, pcc, boa, chase, hurawatch, imdb, youtube])
        all_categories = [search, school, finance, entertainment, video_streaming, all_bookmarks]

        return all_bookmarks, all_categories

    @classmethod
    def add_category(cls, category):
        cls.connect()
        cls.__categories_collection.update_one({ "_id": category.get_key() }, { "$set": category.to_dict() }, upsert=True)

    @classmethod
    def add_bookmark(cls, bookmark):
        cls.connect()
        cls.__bookmarks_collection.update_one({ "_id": bookmark.get_key() }, { "$set": bookmark.to_dict() }, upsert=True)

    @classmethod
    def delete_category(cls, category):
        cls.connect()
        cls.__categories_collection.delete_one({ "_id": category.get_key() })


if __name__ == "__main__":
    Database.rebuild_data()
    Database.read_bookmarks()
    Database.read_categories()