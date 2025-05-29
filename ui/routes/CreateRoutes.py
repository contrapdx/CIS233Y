from ui.WebUI import WebUI
from flask import render_template, request
from logic.GamesLibrary import GamesLibrary
from logic.VideoGame import VideoGame
from logic.FightingGame import FightingGame

class CreateRoutes(WebUI):
    __app = WebUI.get_app()

    @staticmethod
    @__app.route('/create_library')
    def create_library():
        return render_template("create/create_library.html")

    @staticmethod
    @__app.route('/do_create_library', methods=['GET', 'POST'])
    def do_create_library():
        name, error = WebUI.validate_field(object_name="library", field_name="name")
        if name is None:
            return error
        key = name.lower()
        library = WebUI.lookup_library(key)
        if library is not None:
            return render_template(
                "error.html",
                message_header="Library already exists!",
                message_body=f"A library named {name} already exists. Please choose another name and try again."
            )
        if "icon" in request.form:
            icon = request.form["icon"].strip()
        else:
            icon = ""
        if "description" in request.form:
            description = request.form["description"].strip()
        else:
            description = ""
        library = GamesLibrary(name=name, games=[], icon=icon, description=description,
                               user_key=WebUI.get_user_key(), library_map=WebUI.get_library_map(), save=True)
        WebUI.get_all_libraries().append(library)
        return render_template("create/confirm_library_created.html", library=library)

    @staticmethod
    @__app.route('/create_video_game')
    def create_video_game():
        return render_template("create/create_video_game.html")

    @staticmethod
    @__app.route('/do_create_video_game', methods=['GET', 'POST'])
    def do_create_video_game():
        title, error = WebUI.validate_field(object_name="video game", field_name="title")
        if title is None:
            return error
        release_year, error = WebUI.validate_field(object_name="video game", field_name="release_year")
        if release_year is None:
            return error
        key = VideoGame.make_key(title, release_year).lower()
        game = WebUI.lookup_game(key)
        if game is not None:
            return render_template(
                "error.html",
                message_header="Game already exists!",
                message_body=f"The game '{title} ({release_year})' already exists. Please choose another game and try again."
            )
        developer, error = WebUI.validate_field(object_name="video game", field_name="developer")
        if developer is None:
            return error
        genre, error = WebUI.validate_field(object_name="video game", field_name="genre")
        if genre is None:
            return error
        if "series" in request.form:
            series = request.form["series"].strip()
        else:
            series = ""
        game = VideoGame(title=title, release_year=release_year,
                         developer=developer, genre=genre, series=series,
                         user_key=WebUI.get_user_key(), game_map=WebUI.get_game_map(), save=True)
        WebUI.get_all_games().append(game)
        return render_template("create/confirm_video_game_created.html", game=game)

    @staticmethod
    @__app.route('/create_fighting_game')
    def create_fighting_game():
        return render_template("create/create_fighting_game.html")

    @staticmethod
    @__app.route('/do_create_fighting_game', methods=['GET', 'POST'])
    def do_create_fighting_game():
        # title, release_year, developer, series, subgenre, shorthand, evo_appearances
        title, error = WebUI.validate_field(object_name="fighting game", field_name="title")
        if title is None:
            return error
        shorthand, error = WebUI.validate_field(object_name="fighting game", field_name="shorthand")
        key = FightingGame.make_key(title, shorthand).lower()
        game = WebUI.lookup_game(key)
        if game is not None:
            return render_template(
                "error.html",
                message_header="Game already exists!",
                message_body=f"The game '{title} ({shorthand})' already exists. "
                             f"Please choose another game and try again."
            )
        subgenre, error = WebUI.validate_field(object_name="fighting game", field_name="subgenre")
        if subgenre is None:
            return error
        release_year, error = WebUI.validate_field(object_name="fighting game", field_name="release_year")
        if release_year is None:
            return error
        developer, error = WebUI.validate_field(object_name="fighting game", field_name="developer")
        if developer is None:
            return error
        evo_appearances, error = WebUI.validate_field(object_name="fighting game", field_name="evo_appearances")
        if evo_appearances is None:
            return error
        if "series" in request.form:
            series = request.form["series"].strip()
        else:
            series = ""
        game = FightingGame(title=title, shorthand=shorthand, release_year=release_year, developer=developer,
                            subgenre=subgenre, evo_appearances=evo_appearances, series=series, genre="fighting game",
                            user_key=WebUI.get_user_key(), game_map=WebUI.get_game_map(), save=True)
        WebUI.get_all_games().append(game)
        return render_template("create/confirm_fighting_game_created.html", game=game)

    @staticmethod
    @__app.route("/join_libraries")
    def join_libraries():
        return render_template("create/join_libraries.html", libraries=WebUI.get_all_libraries())

    @staticmethod
    @__app.route("/do_join_libraries", methods=['GET', 'POST'])
    def do_join_libraries():
        first_key, error = WebUI.validate_field(object_name="first library", field_name="first_library")
        if first_key is None:
            return error
        second_key, error = WebUI.validate_field(object_name="second library", field_name="second_library")
        if second_key is None:
            return error
        first_library = WebUI.lookup_library(first_key.lower())
        if first_library is None:
            return render_template(
                "error.html",
                message_header=f"First library {first_key} not found.",
                message_body=f"The first library {first_key} does not exist. "
                             f"Please choose another library and try again."
            )
        second_library = WebUI.lookup_library(second_key.lower())
        if second_library is None:
            return render_template(
                "error.html",
                message_header=f"First library {second_key} not found.",
                message_body=f"The first library {second_key} does not exist. "
                             f"Please choose another library and try again."
            )
        new_key = f"{first_library.get_name()} / {second_library.get_name()}"
        new_library =  WebUI.lookup_library(new_key.lower())
        if new_library is not None:
            return render_template(
                "error.html",
                message_header=f"Library {new_key} already exists.",
                message_body=f"The library {new_key} already exists."
            )
        new_library = first_library + second_library
        WebUI.get_all_libraries().append(new_library)
        return render_template(
            "create/confirm_libraries_joined.html",
            first_library=first_library,
            second_library=second_library,
            new_library=new_library
        )
