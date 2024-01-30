from logic.Site import Site
from ui.input_validation import select_item, input_string
from logic.Category import Category


class ConsoleUI:
    __all_bookmarks = None
    __all_categories = None

    CHOICES = ["p", "l", "s", "a", "d", "x"]

    @staticmethod
    def print_menu():
        print()
        print("Options for the bookmark manager:")
        print("  p: Print the bookmarks.")
        print("  l: Print the list of categories.")
        print("  s: Print the bookmarks for a selected category.")
        print("  a: Add a new category.")
        print("  d: Delete a category.")
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

        print("Goodbye!")

if __name__ == "__main__":
    ConsoleUI.init()
    ConsoleUI.run()
