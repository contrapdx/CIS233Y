from ui.WebUI import WebUI
from flask import render_template, request
from logic.GamesLibrary import GamesLibrary

class PrintRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route('/print_libraries')
    def print_libraries():
        return render_template("print/print_libraries.html", libraries=WebUI.get_all_libraries())

    @staticmethod
    @__app.route('/print_library')
    def print_library():
        if "library" not in request.args:
            return render_template(
                "error.html",
                message_header="Library not specified!",
                message_body="No library specified. Please check the URL and try again."
            )
        name = request.args["library"]
        key = GamesLibrary.make_key(name)
        library = WebUI.lookup_library(key)
        if library is None:
            return render_template(
                "error.html",
                message_header="Library not found!",
                message_body=f"The library named '{key}' was not found. Please check the URL and try again."
            )
        return render_template("print/print_library.html", library=library)

    @staticmethod
    @__app.route('/show_library_contents')
    def show_library_contents():
        return render_template(
            "print/show_library_contents.html",
            libraries=WebUI.get_all_libraries())
