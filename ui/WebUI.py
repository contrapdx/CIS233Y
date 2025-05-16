from flask import Flask, render_template, request
from logic.GamesLibrary import GamesLibrary

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
            "create_library": "Create a new library.",
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
    def get_app(cls):
        return cls.__app

    @classmethod
    def get_all_libraries(cls):
        return cls.__all_libraries

    @classmethod
    def get_all_games(cls):
        return cls.__all_games

    @classmethod
    def init(cls):
        cls.__all_games, cls.__all_libraries = GamesLibrary.read_data()

    @staticmethod
    @__app.route('/')
    @__app.route('/index')
    @__app.route('/index.html')
    @__app.route('/index.php')
    def homepage():
        return render_template("homepage.html", options=WebUI.MENU)

    @classmethod
    def run(cls):
        from ui.PrintRoutes import PrintRoutes
        from ui.CreateRoutes import CreateRoutes

        cls.__app.run(host="0.0.0.0", port=8000)
