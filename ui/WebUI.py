from flask import Flask, render_template, request
from logic.Category import Category

class WebUI:
    __app = Flask(__name__)
    __all_bookmarks = None
    __all_categories = None

    @classmethod
    def init(cls):
        cls.__all_bookmarks, cls.__all_categories = Category.read_data()

    @staticmethod
    @__app.route('/print_bookmarks')
    def print_bookmarks():
        return render_template("print_bookmarks.html", bookmarks=WebUI.__all_bookmarks)

    @staticmethod
    @__app.route('/print_categories')
    def print_categories():
        return render_template("print_categories.html", categories=WebUI.__all_categories)

    @staticmethod
    @__app.route('/print_category')
    def print_category():
        key = request.args["category"]
        try:
            category = Category.lookup(key)
            return "Found category " + category.get_name()
        except KeyError:
            pass
        return render_template(
            "error.html",
            error_header="Invalid category!",
            error_message="<p>Couldn't find category key!")

    @staticmethod
    @__app.route('/')
    @__app.route('/index.html')
    @__app.route('/main.html')
    def hello():
        return '<h1>Hello World!</h1><p>Hello World!</p>'

    @classmethod
    def run(cls):
        cls.__app.run(host='0.0.0.0')


if __name__ == '__main__':
    WebUI.init()
    WebUI.run()
