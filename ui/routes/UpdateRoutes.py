from ui.WebUI import WebUI
from flask import render_template, request
from logic.GamesLibrary import GamesLibrary
from logic.VideoGame import VideoGame
from logic.FightingGame import FightingGame

class UpdateRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route("/update_video_game_series")
    def update_game_series():
        return render_template("update/update_video_game_series.html", games=WebUI.get_all_games())

    @staticmethod
    @__app.route("/do_update_video_game_series", methods=["GET", "POST"])
    def do_update_video_game_series():
        key, error = WebUI.validate_field(object_name="video game", field_name="game")
        if key is None:
            return error
        game = WebUI.lookup_game(key)
        if game is None:
            return render_template(
                "error.html",
                message_header="Game does not exist!",
                message_body=f"The game {key} does not exist. Please choose another game and try again."
            )
        if "series" in request.form:
            series = request.form["series"].strip()
        else:
            series = ""
        game.update_series(series)
        return render_template("update/confirm_series_updated.html", game=game)

    @staticmethod
    @__app.route("/add_video_game_to_library")
    def add_video_game_to_library():
        return render_template(
            "update/add_video_game_to_library.html",
            games=WebUI.get_all_games(), libraries=WebUI.get_all_libraries()
        )

    @staticmethod
    @__app.route("/do_add_video_game_to_library", methods=["GET", "POST"])
    def do_add_video_game_to_library():
        game_key, error = WebUI.validate_field(object_name="video game", field_name="game")
        if game_key is None:
            return error
        game = WebUI.lookup_game(game_key)
        if game is None:
            return render_template(
                "error.html",
                message_header="Game does not exist!",
                message_body=f"The game {game_key} does not exist. Please choose another game and try again."
            )
        library_key, error = WebUI.validate_field(object_name="library", field_name="library")
        if library_key is None:
            return error
        library = WebUI.lookup_library(library_key.lower())
        if library is None:
            return render_template(
                "error.html",
                message_header=f"Library {library_key} not found.",
                message_body=f"The library {library_key} does not exist. "
                             f"Please choose another library and try again."
            )
        if game in library:
            return render_template(
                "error.html",
                message_header=f"Video Game is already in Library.",
                message_body=f"Video game '{game.get_printable_key()}' is already in library '{library.get_name()}'. "
                             f"Please choose another game and library and try again."
            )
        library.append(game)
        return render_template("update/confirm_video_game_added_to_library.html",
                               game=game, library=library)

    @staticmethod
    @__app.route("/remove_video_game_from_library")
    def remove_video_game_from_library():
        return render_template(
            "update/remove_video_game_from_library.html",
            games=WebUI.get_all_games(), libraries=WebUI.get_all_libraries()
        )

    @staticmethod
    @__app.route("/do_remove_video_game_from_library", methods=["GET", "POST"])
    def do_remove_video_game_from_library():
        game_key, error = WebUI.validate_field(object_name="video game", field_name="game")
        if game_key is None:
            return error
        game = WebUI.lookup_game(game_key)
        if game is None:
            return render_template(
                "error.html",
                message_header="Game does not exist!",
                message_body=f"The game {game_key} does not exist. Please choose another game and try again."
            )
        library_key, error = WebUI.validate_field(object_name="library", field_name="library")
        if library_key is None:
            return error
        library = WebUI.lookup_library(library_key.lower())
        if library.get_name() == GamesLibrary.ALL_GAMES:
            return render_template(
                "error.html",
                message_header=f"Cannot remove game.",
                message_body=f"Cannot remove games from the {GamesLibrary.ALL_GAMES} library."
            )
        if library is None:
            return render_template(
                "error.html",
                message_header=f"Library {library_key} not found.",
                message_body=f"The library {library_key} does not exist. "
                             f"Please choose another library and try again."
            )
        if game not in library:
            return render_template(
                "error.html",
                message_header=f"Video Game is not in Library.",
                message_body=f"Video game '{game.get_printable_key()}' is not in library '{library.get_name()}'. "
                             f"Please choose another game and library and try again."
            )
        library.remove(game)
        return render_template("update/confirm_video_game_removed_from_library.html",
                               game=game, library=library)
