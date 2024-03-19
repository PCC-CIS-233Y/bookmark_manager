from flask import Flask, render_template, request, session
from flask_session import Session
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
            ["create_site_form?registered=False", "Create a New Site"],
            ["create_site_form?registered=True", "Create a Registered Site"],
            ["create_category_form", "Create a Category"],
            ["join_categories_form", "Join Two Categories"]
        ],
        "Update": [
            ["insert_site_into_category_form", "Insert bookmark into category."],
            ["update_site_form", "Update the Description for a Bookmark."]
        ],
        "Delete": [
            ["delete_site_from_category_form", "Delete bookmark from category."],
            ["delete_category_form", "Delete a Category"]
        ]
    }

    @classmethod
    def init(cls):
        cls.__all_bookmarks, cls.__all_categories = Category.read_data()

    @staticmethod
    @__app.route("/get_user")
    def get_user():
        if "username" in session:
            return session["username"]
        else:
            return "No user"

    @staticmethod
    @__app.route("/login")
    def login():
        from logic.User import User

        username = request.args["username"]
        password = request.args["password"]
        user = User.read_user(username)
        if user is None:
            return "Login failed"
        result = user.verify_user(password)
        if result:
            return "Login successful!"
        else:
            return "Login failed"

    @staticmethod
    @__app.route("/set_user")
    def set_user():
        if "username" in request.args:
            username = request.args["username"]
            session["username"] = username
            return "OK"
        else:
            return "No username specified"


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
        categories = WebUI.__all_categories
        categories.sort(key=lambda x: x.get_name().lower())
        return render_template("print/print_categories.html", categories=categories)

    @staticmethod
    @__app.route("/create_site_form")
    def create_site_form():
        if "registered" in request.args:
            registered = request.args["registered"]
        else:
            registered = "False"
        return render_template("create/create_site_form.html", registered=registered)

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

        if "registered" in request.form:
            registered = request.form["registered"]
        else:
            registered = "False"

        if registered == "True":
            if "username" not in request.form:
                return render_template("general/error.html", error_header="Error! Username not specified!",
                                       error_message="<p>The request you sent does not include a username. Often, this is because"
                                                     " you are accessing the create_site url directly, instead of submitting the form.</p>")
            username = request.form["url"].strip()
            if username == "":
                return render_template("general/error.html", error_header="Error! Username cannot be empty!",
                                       error_message="<p>The request you sent does not include a valid username. Please go back and update your form.</p>")

            if "password" not in request.form:
                password = ""
            else:
                password = request.form["password"]

        try:
            site = Site.lookup(url)
            return render_template("general/error.html", error_header="Error! Bookmark already exists!",
                                   error_message="<p>The site you are trying to add is already in the bookmark manager.</p>")
        except KeyError:
            pass
        if registered == "False":
            site = Site(url, title, description, str(datetime.now()))
        else:
            site = RegisteredSite(url, title, description, str(datetime.now()), username, password)
        WebUI.__all_bookmarks.add(site)
        site.add_to_database()
        WebUI.__all_bookmarks.add_to_database()
        return render_template("create/confirm_new_site.html", site=site)

    @staticmethod
    @__app.route("/create_category_form")
    def create_category_form():
        return render_template("create/create_category_form.html")

    @staticmethod
    @__app.route("/create_category", methods=["GET", "POST"])
    def create_category():
        if "name" not in request.form:
            return render_template("general/error.html", error_header="Error! Name not specified!",
                                   error_message="<p>The request you sent does not include a name. Often, this is because"
                                                 " you are accessing the create_site url directly, instead of submitting the form.</p>")
        name = request.form["name"].strip()
        if name == "":
            return render_template("general/error.html", error_header="Error! Name cannot be empty!",
                                   error_message="<p>The request you sent does not include a valid name. Please go back and update your form.</p>")
        if "description" in request.form:
            description = request.form["description"].strip()
        else:
            description = ""

        try:
            category = Category.lookup(name)
            return render_template("general/error.html", error_header="Error! Category already exists!",
                                   error_message="<p>The category you are trying to add is already in the bookmark manager.</p>")
        except KeyError:
            pass
        category = Category(name, description, [])
        WebUI.__all_categories.append(category)
        category.add_to_database()
        return render_template("create/confirm_new_category.html", category=category)

    @staticmethod
    @__app.route("/insert_site_into_category_form")
    def insert_site_into_category_form():
        bookmarks = WebUI.__all_bookmarks.get_bookmarks()
        bookmarks.sort(key=lambda x: x.get_title().lower())
        categories = WebUI.__all_categories
        categories.sort(key=lambda x: x.get_name().lower())
        return render_template(
            "update/insert_site_into_category_form.html",
            bookmarks=bookmarks, categories=categories
        )

    @staticmethod
    @__app.route("/insert_site_into_category")
    def insert_site_into_category():
        if "category" in request.args:
            try:
                category = Category.lookup(request.args["category"])
            except KeyError:
                return render_template("general/error.html", error_header="Error! Unknown Category.",
                                       error_message=f"<p>The category <b>{request.args['category']}</b> does not exist. Please select a valid category.")
        else:
            return render_template("general/error.html", error_header="Error! Category not Specified.",
                                   error_message=f"<p>The category was not specified. Please select a valid category.")

        if "bookmark" in request.args:
            try:
                bookmark = Site.lookup(request.args["bookmark"])
            except KeyError:
                return render_template("general/error.html", error_header="Error! Unknown Site.",
                                       error_message=f"<p>The site <b>{request.args['bookmark']}</b> does not exist. Please select a valid site.")
        else:
            return render_template("general/error.html", error_header="Error! Site not Specified.",
                                   error_message=f"<p>The site was not specified. Please select a valid site.")

        if bookmark in category:
            return render_template(
                "general/error.html",
                error_header="Error! Site already in Category.",
                error_message=f"<p>The site <b>{ bookmark.get_title() }</b> is already in the category <b>{category.get_name() }</b>.")

        category.add(bookmark)
        category.add_to_database()
        return render_template("update/confirm_insert_site_into_category.html", bookmark=bookmark, category=category)


    @staticmethod
    @__app.route("/delete_category_form")
    def delete_category_form():
        categories = WebUI.__all_categories
        categories.sort(key=lambda x: x.get_name().lower())
        return render_template("delete/delete_category_form.html", categories=categories)

    @staticmethod
    @__app.route("/delete_category")
    def delete_category():
        if "category" not in request.args:
            return render_template("general/error.html", error_header="Error! Category name not specified!",
                                   error_message="<p>The request you sent does not include a Category name. Often, this is because"
                                                 " you are accessing the create_site url directly, instead of submitting the form.</p>")
        key = request.args["category"].strip()
        if key == "":
            return render_template("general/error.html", error_header="Error! Category name cannot be empty!",
                                   error_message="<p>The request you sent does not include a valid Category name. Please go back and update your form.</p>")
        try:
            category = Category.lookup(key)
        except KeyError:
            return render_template("general/error.html", error_header="Error! Category does not exists!",
                                   error_message="<p>The category that you are trying to delete does not exist.</p>")

        WebUI.__all_categories.remove(category)
        category.delete()
        return render_template("delete/confirm_delete_category.html", category=category)

    @staticmethod
    @__app.route("/delete_site_from_category_form")
    def delete_site_from_category_form():
        bookmarks = WebUI.__all_bookmarks.get_bookmarks()
        bookmarks.sort(key=lambda x: x.get_title().lower())
        categories = WebUI.__all_categories
        categories.sort(key=lambda x: x.get_name().lower())
        return render_template(
            "delete/delete_site_from_category_form.html",
            bookmarks=bookmarks, categories=categories
        )

    @staticmethod
    @__app.route("/delete_site_from_category")
    def delete_site_from_category():
        if "category" in request.args:
            try:
                category = Category.lookup(request.args["category"])
            except KeyError:
                return render_template("general/error.html", error_header="Error! Unknown Category.",
                                       error_message=f"<p>The category <b>{request.args['category']}</b> does not exist. Please select a valid category.")
        else:
            return render_template("general/error.html", error_header="Error! Category not Specified.",
                                   error_message=f"<p>The category was not specified. Please select a valid category.")

        if "bookmark" in request.args:
            try:
                bookmark = Site.lookup(request.args["bookmark"])
            except KeyError:
                return render_template("general/error.html", error_header="Error! Unknown Site.",
                                       error_message=f"<p>The site <b>{request.args['bookmark']}</b> does not exist. Please select a valid site.")
        else:
            return render_template("general/error.html", error_header="Error! Site not Specified.",
                                   error_message=f"<p>The site was not specified. Please select a valid site.")

        if bookmark not in category:
            return render_template(
                "general/error.html",
                error_header="Error! Site is not in Category.",
                error_message=f"<p>The site <b>{ bookmark.get_title() }</b> is not in the category <b>{category.get_name() }</b>.")

        category.remove(bookmark)
        category.add_to_database()
        return render_template("delete/confirm_delete_site_from_category.html", bookmark=bookmark, category=category)


    @staticmethod
    @__app.route("/update_site_form")
    def update_site_form():
        bookmarks = WebUI.__all_bookmarks.get_bookmarks()
        bookmarks.sort(key=lambda x: x.get_title().lower())
        return render_template(
            "update/update_site_form.html",
            bookmarks=bookmarks
        )

    @staticmethod
    @__app.route("/update_site")
    def update_site():
        if "bookmark" in request.args:
            try:
                bookmark = Site.lookup(request.args["bookmark"])
            except KeyError:
                return render_template("general/error.html", error_header="Error! Unknown Site.",
                                       error_message=f"<p>The site <b>{request.args['bookmark']}</b> does not exist. Please select a valid site.")
        else:
            return render_template("general/error.html", error_header="Error! Site not Specified.",
                                   error_message=f"<p>The site was not specified. Please select a valid site.")

        if "description" in request.args:
            description = request.args["description"]
        else:
            description = ""

        bookmark.set_description(description)
        bookmark.add_to_database()
        return render_template("update/confirm_update_site.html", bookmark=bookmark)


    @staticmethod
    @__app.route("/join_categories_form")
    def join_categories_form():
        categories = WebUI.__all_categories
        categories.sort(key=lambda x: x.get_name().lower())
        return render_template("create/join_categories_form.html", categories=categories)

    @staticmethod
    @__app.route('/join_categories')
    def join_categories():
        if "first_category" in request.args:
            try:
                first_category = Category.lookup(request.args["first_category"])
            except KeyError:
                return render_template("general/error.html", error_header="Error! Unknown Category.",
                                       error_message=f"<p>The category <b>{request.args['first_category']}</b> does not exist. Please select a valid category.")
        else:
            return render_template("general/error.html", error_header="Error! First Category not Specified.",
                                    error_message=f"<p>The first category was not specified.")
        if "second_category" in request.args:
            try:
                second_category = Category.lookup(request.args["second_category"])
            except KeyError:
                return render_template("general/error.html", error_header="Error! Unknown Category.",
                                       error_message=f"<p>The category <b>{request.args['second_category']}</b> does not exist. Please select a valid category.")
        else:
            return render_template("general/error.html", error_header="Error! Second Category not Specified.",
                                    error_message=f"<p>The second category was not specified.")

        try:
            new_category = first_category + second_category
        except Exception as e:
            return render_template("general/error.html", error_header="Error! Error joining categories",
                                   error_message=f"<p>Error joining categories: {e.message}</p>")

        WebUI.__all_categories.append(new_category)
        new_category.add_to_database()

        return render_template("create/confirm_join_categories.html", first_category=first_category, second_category=second_category, new_category=new_category)

    @staticmethod
    @__app.route('/')
    @__app.route('/index.html')
    @__app.route('/main.html')
    def hello():
        return render_template("general/main.html", routes=WebUI.ROUTES)

    @classmethod
    def run(cls):
        cls.__app.secret_key = "This is a secret key"
        cls.__app.config["SESSION_TYPE"] = "filesystem"
        cls.__app.run(host='0.0.0.0', port=8443, ssl_context=("cert.pem", "key.pem"))


if __name__ == '__main__':
    WebUI.init()
    WebUI.run()
