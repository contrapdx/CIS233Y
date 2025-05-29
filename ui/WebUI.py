from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from logic.GamesLibrary import GamesLibrary
from logic.UserState import UserState
import os
import bcrypt

class WebUI:
    __all_games = None
    __all_libraries = None
    __app = Flask(__name__)
    ALLOWED_PATHS = [
        "/login",
        "/do_login",
        "/static/gamebox.css"
    ]
    MENU = {
        "Print":{
            "print_library?library=All%20Games": "Print a list of all games.",
            "print_libraries": "Print a list of all libraries.",
            "show_library_contents": "Select a library and show its contents."
        },
        "Create":{
            "create_video_game": "Create a new video game.",
            "create_fighting_game": "Create a new fighting game.",
            "create_library": "Create a new library.",
            "join_libraries": "Join a library with another library."
        },
        "Update":{
            "update_video_game_series": "Update a game's series.",
            "add_video_game_to_library": "Add a game to a library.",
            "remove_video_game_from_library": "Remove a game from a library."
        },
        "Delete":{
            "delete_video_game": "Delete a game.",
            "delete_library": "Delete a library."
        }
    }

    @classmethod
    def get_app(cls):
        return cls.__app

    @classmethod
    def get_user(cls):
        if "user" in session:
            return session["user"]
        return None

    @classmethod
    def get_user_key(cls):
        user = cls.get_user()
        if user is None:
            return None
        return user.get_key()

    @classmethod
    def get_all_libraries(cls):
        user_state = UserState.lookup(cls.get_user_key())
        if user_state is not None:
            return user_state.get_all_libraries()
        return None

    @classmethod
    def get_all_games(cls):
        user_state = UserState.lookup(cls.get_user_key())
        if user_state is not None:
            return user_state.get_all_games()
        return

    @classmethod
    def get_library_map(cls):
        user_state = UserState.lookup(cls.get_user_key())
        if user_state is not None:
            return user_state.get_library_map()
        return

    @classmethod
    def get_game_map(cls):
        user_state = UserState.lookup(cls.get_user_key())
        if user_state is not None:
            return user_state.get_game_map()
        return

    @classmethod
    def login(cls, user):
        session["user"] = user
        UserState(user)

    @classmethod
    def logout(cls):
        UserState.logout(WebUI.get_user_key())

    @classmethod
    def lookup_library(cls, key):
        user_state = UserState.lookup(cls.get_user_key())
        if user_state is not None:
            return user_state.lookup_library(key)

    @classmethod
    def lookup_game(cls, key):
        user_state = UserState.lookup(cls.get_user_key())
        if user_state is not None:
            return user_state.lookup_game(key)

    @classmethod
    def validate_field(cls, object_name, field_name):
        if field_name not in request.form:
            return None, render_template(
                "error.html",
                message_header=f"{object_name} {field_name} not specified!",
                message_body=f"No {object_name} {field_name} specified. Please check the form and try again."
            )
        field_value = request.form[field_name].strip()
        if field_value == "":
            return None, render_template(
                "error.html",
                message_header=f"{object_name} {field_name} not specified!",
                message_body=f"{object_name} {field_name} not specified. Please check the form and try again."
            )
        return field_value, None

    @staticmethod
    @__app.before_request
    def before_request():
        if "user" not in session:
            if request.path not in WebUI.ALLOWED_PATHS:
                return redirect(url_for("login"))
            return
        user_state = UserState.lookup(WebUI.get_user_key())
        if user_state is None:
            UserState(WebUI.get_user())

    @staticmethod
    @__app.route('/index')
    @__app.route('/index.html')
    @__app.route('/index.php')
    @__app.route('/')
    def homepage():
        return render_template("homepage.html", options=WebUI.MENU)

    @classmethod
    def run(cls):
        from ui.routes.PrintRoutes import PrintRoutes
        from ui.routes.CreateRoutes import CreateRoutes
        from ui.routes.UpdateRoutes import UpdateRoutes
        from ui.routes.DeleteRoutes import DeleteRoutes
        from ui.routes.UserRoutes import UserRoutes

        if "APPDATA" in os.environ:
            path = os.environ["APPDATA"]
        elif "HOME" in os.environ:
            path = os.environ["HOME"]
        else:
            raise Exception("Couldn't find config folder.")

        cls.__app.secret_key = bcrypt.gensalt()
        cls.__app.config["SESSION_TYPE"] = "filesystem"
        Session(cls.__app)
        print("Web server launched successfully")
        cls.__app.run(host="0.0.0.0", port=8443, ssl_context=(path + "/game_box/cert.pem", path + "/game_box/key.pem"))
