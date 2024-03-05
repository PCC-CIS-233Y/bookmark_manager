from flask import Flask, render_template, request
from logic.Site import Site
from logic.RegisteredSite import RegisteredSite
from logic.Category import Category
from datetime import datetime

class WebUI:
    __app = Flask(__name__)
    __all_bookmarks = None
    __all_categories = None
    ROUTES = {
        "Print": [
            ["print_bookmarks", "Print the bookmarks."],
            ["print_categories", "Print the list of categories."],
            ["print_bookmarks_form", "Print the bookmarks for a selected category."]
        ],
        "Create": [
            ["create_site_form", "Create a New Site"],
            ["create_registered_site_form", "Create a Registered Site"],
            ["create_category_form", "Create a Category"]
        ],
        "Update": [
            ["insert_site_into_category", "Insert bookmark into category."]
        ]
    }

    @classmethod
    def init(cls):
        cls.__all_bookmarks, cls.__all_categories = Category.read_data()

    @staticmethod
    @__app.route("/print_bookmarks_form")
    def print_bookmarks_form():
        return render_template("print/print_bookmarks_form.html", categories=WebUI.__all_categories)

    @staticmethod
    @__app.route('/print_bookmarks')
    def print_bookmarks():
        if "category" in request.args:
            try:
                category = Category.lookup(request.args["category"])
            except KeyError:
                return render_template("general/error.html", error_header="Error! Unknown Category.",
                                       error_message=f"<p>The category <b>{request.args['category']}</b> does not exist. Please select a valid category.")
        else:
            category = WebUI.__all_bookmarks
        return render_template("print/print_bookmarks.html", category=category)

    @staticmethod
    @__app.route('/print_categories')
    def print_categories():
        return render_template("print/print_categories.html", categories=WebUI.__all_categories)

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
            "general/error.html",
            error_header="Invalid category!",
            error_message="<p>Couldn't find category key!")

    @staticmethod
    @__app.route("/create_site_form")
    def create_site_form():
        return render_template("create/create_site_form.html")

    @staticmethod
    @__app.route("/create_site", methods=["GET", "POST"])
    def create_site():
        if "url" not in request.form:
            return render_template("general/error.html", error_header="Error! URL not specified!",
                                   error_message="<p>The request you sent does not include a URL. Often, this is because"
                                                 " you are accessing the create_site url directly, instead of submitting the form.</p>")
        url = request.form["url"].strip()
        if url == "":
            return render_template("general/error.html", error_header="Error! URL cannot be empty!",
                                   error_message="<p>The request you sent does not include a valid URL. Please go back and update your form.</p>")
        if "title" not in request.form:
            return render_template("general/error.html", error_header="Error! Title not specified!",
                                   error_message="<p>The request you sent does not include a title. Often, this is because"
                                                 " you are accessing the create_site url directly, instead of submitting the form.</p>")
        title = request.form["title"].strip()
        if title == "":
            return render_template("general/error.html", error_header="Error! Title cannot be empty!",
                                   error_message="<p>The request you sent does not include a valid title. Please go back and update your form.</p>")
        if "description" in request.form:
            description = request.form["description"].strip()
        else:
            description = ""

        site = Site(url, title, description, str(datetime.now()))
        WebUI.__all_bookmarks.add(site)
        site.add_to_database()
        WebUI.__all_bookmarks.add_to_database()
        return render_template("create/confirm_new_site.html", site=site)

    @staticmethod
    @__app.route('/')
    @__app.route('/index.html')
    @__app.route('/main.html')
    def hello():
        return render_template("general/main.html", routes=WebUI.ROUTES)

    @classmethod
    def run(cls):
        cls.__app.run(host='0.0.0.0')


if __name__ == '__main__':
    WebUI.init()
    WebUI.run()
