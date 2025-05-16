from flask import Flask, render_template, request
from logic.GamesLibrary import GamesLibrary
from logic.VideoGame import VideoGame

class WebUI:
    __all_games = None
    __all_libraries = None
    __app = Flask(__name__)

    MENU = {
        "Print":{
            "print_library?library=All%20Games": "Print a list of all games.",
            "print_libraries": "Print a list of all libraries."
        },
        "Create":{
            "create_game": "Create a new game.",
            "create_libraries": "Create a new library.",
            "join_libraries": "Join a library with another library."
        },
        "Update":{
            "update_game_series": "Update a game's series.",
            "add_game_to_library": "Add a game to a library.",
            "remove_game_from_library": "Remove a game from a library."
        },
        "Delete":{
            "delete_game": "Delete a game.",
            "delete_library": "Delete a library."
        }
    }

    @classmethod
    def init(cls):
        cls.__all_games, cls.__all_libraries = GamesLibrary.read_data()

    @__app.route('/')
    @__app.route('/index')
    @__app.route('/index.html')
    @__app.route('/index.php')
    @staticmethod
    def homepage():
        return render_template("homepage.html", options=WebUI.MENU)

    @__app.route('/print_libraries')
    @staticmethod
    def print_libraries():
        return render_template("print/print_libraries.html", libraries=WebUI.__all_libraries)

    @__app.route('/print_library')
    @staticmethod
    def print_library():
        if "library" not in request.args:
            return render_template(
                "error.html",
                message_header="Library not specified!",
                message_body="No library specified. Please check the URL and try again."
            )
        key = request.args["library"]
        library = GamesLibrary.lookup(key)
        if library is None:
            return render_template(
                "error.html",
                message_header="Library not found!",
                message_body=f"The library named '{key}' was not found. Please check the URL and try again."
            )
        return render_template("print/print_library.html", library=library)

    @classmethod
    def run(cls):
        cls.__app.run(port=8000)

if __name__ == '__main__':
    WebUI.init()
    WebUI.run()
