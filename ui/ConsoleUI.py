from logic.Site import Site
from logic.RegisteredSite import RegisteredSite
from ui.input_validation import select_item, input_string, y_or_n
from logic.Category import Category
from datetime import datetime

class ConsoleUI:
    __all_bookmarks = None
    __all_categories = None

    CHOICES = ["p", "l", "s", "a", "d", "b", "i", "r", "u", "j", "x"]

    @staticmethod
    def print_menu():
        print()
        print("Options for the bookmark manager:")
        print("  p: Print the bookmarks.")
        print("  l: Print the list of categories.")
        print("  s: Print the bookmarks for a selected category.")
        print("  a: Add a new category.")
        print("  d: Delete a category.")
        print("  b: Make a new bookmark.")
        print("  i: Insert bookmark into category.")
        print("  r: Remove a bookmark from a category.")
        print("  u: Update the description for a bookmark.")
        print("  j: Join two categories together.")
        print("  x: Exit the program.")

    @classmethod
    def init(cls):
        cls.__all_bookmarks, cls.__all_categories = Category.read_data()

    @classmethod
    def print_bookmarks(cls):
        for bookmark in cls.__all_bookmarks:
            print(bookmark)

    @classmethod
    def print_categories(cls):
        for category in cls.__all_categories:
            print(category.get_name())

    @classmethod
    def select_category(cls):
        names = [category.get_name() for category in cls.__all_categories] + ["exit"]
        prompt_string = "Current list of categories:"
        for name in names:
            prompt_string += "\n    " + name
        prompt_string += "\nPlease select an item from the list: "
        selected = select_item(prompt=prompt_string, error="Please select an item from the list!", choices=names)
        if selected == "exit":
            return None
        print("Selected:", selected)
        selected_category = Category.lookup(selected)
        return selected_category

    @classmethod
    def select_bookmark(cls, category=None):
        if category is None:
            category = cls.__all_bookmarks
        urls = [bookmark.get_url() for bookmark in category] + ["exit"]
        prompt_string = "Current list of bookmarks:"
        for url in urls:
            prompt_string += "\n    " + url
        prompt_string += "\nPlease select an item from the list: "
        selected = select_item(prompt=prompt_string, error="Please select an item from the list!", choices=urls)
        if selected == "exit":
            return None
        print("Selected:", selected)
        selected_bookmark = Site.lookup(selected)
        return selected_bookmark

    @classmethod
    def print_selected_category(cls):
        selected_category = cls.select_category()
        if selected_category is None:
            return
        print(f"Bookmarks for {selected_category.get_name()}:")
        for bookmark in selected_category:
            print("   ", bookmark)

    @classmethod
    def new_category(cls):
        while True:
            name = input_string("Please enter the name for the category: ")
            try:
                category = Category.lookup(name)
                if category is not None:
                    print(f"Error! Category {name} already exists!")
                    continue
            except KeyError:
                pass
            if name.lower() == "exit":
                return
            description = input_string("Please type a description for the category: ")
            category = Category(name, description, [])
            cls.__all_categories.append(category)
            print(f"New category {name} was added!")
            return

    @classmethod
    def delete_category(cls):
        selected_category = cls.select_category()
        if selected_category is None:
            return
        if selected_category.get_name() == Category.ALL_BOOKMARKS:
            print(f"Error! Cannot delete the {Category.ALL_BOOKMARKS} category!")
            return
        if selected_category not in cls.__all_categories:
            print(f"Error! Category {selected_category.get_name()} does not exist!")
            return
        cls.__all_categories.remove(selected_category)

    @classmethod
    def new_bookmark(cls):
        has_account = y_or_n("Do you have an account on the site (y/n)? ")
        if has_account:
            url = input_string("What is the URL for the site: ")
            try:
                site = Site.lookup(url)
                if site is not None:
                    print(f"Site {url} already exists!")
                    return
            except KeyError:
                pass
            title = input_string("What is the title for the bookmark: ")
            description = input_string("Please enter a short description for the bookmark: ")
            username = input_string("What is your username for the account: ")
            password = input_string("What is the password for the account: ")
            site = RegisteredSite(url, title, description, str(datetime.now()), username, password)
        else:
            url = input_string("What is the URL for the site: ")
            try:
                site = Site.lookup(url)
                if site is not None:
                    print(f"Site {url} already exists!")
                    return
            except KeyError:
                pass
            title = input_string("What is the title for the bookmark: ")
            description = input_string("Please enter a short description for the bookmark: ")
            site = Site(url, title, description, str(datetime.now()))
        cls.__all_bookmarks.add(site)

    @classmethod
    def remove_bookmark_from_category(cls):
        category = cls.select_category()
        if category is None:
            return
        if category.get_name() == Category.ALL_BOOKMARKS:
            print("You can't remove a bookmark from All Bookmarks!")
            return
        bookmark = cls.select_bookmark(category)
        if bookmark is None:
            return
        if bookmark not in category:
            print(f"Bookmark {bookmark.get_url()} is not in catgegory {category.get_name()}!")
            return
        category.remove(bookmark)

    @classmethod
    def insert_bookmark_into_category(cls):
        category = cls.select_category()
        if category is None:
            return
        bookmark = cls.select_bookmark()
        if bookmark is None:
            return
        if bookmark in category:
            print(f"Bookmark {bookmark.get_url()} is already in catgegory {category.get_name()}!")
            return
        category.add(bookmark)

    @classmethod
    def update_bookmark_description(cls):
        bookmark = cls.select_bookmark()
        if bookmark is None:
            return
        description = input_string("Please type a new description for the bookmark: ")
        bookmark.set_description(description)

    @classmethod
    def join_categories(cls):
        category1 = cls.select_category()
        if category1 is None:
            return
        category2 = cls.select_category()
        if category2 is None:
            return

        try:
            new_category = category1 + category2
        except Exception as e:
            print(e)
            return

        cls.__all_categories.append(new_category)


    @classmethod
    def run(cls):
        while True:
            cls.print_menu()
            choice = select_item("Please select an option: ", "Please select one of the items above!", choices=cls.CHOICES)
            if choice == "x":
                break
            elif choice == "p":
                cls.print_bookmarks()
            elif choice == "l":
                cls.print_categories()
            elif choice == "s":
                cls.print_selected_category()
            elif choice == "a":
                cls.new_category()
            elif choice == "d":
                cls.delete_category()
            elif choice == "b":
                cls.new_bookmark()
            elif choice == "i":
                cls.insert_bookmark_into_category()
            elif choice == "r":
                cls.remove_bookmark_from_category()
            elif choice == "u":
                cls.update_bookmark_description()
            elif choice == "j":
                cls.join_categories()

        print("Goodbye!")

if __name__ == "__main__":
    ConsoleUI.init()
    ConsoleUI.run()
