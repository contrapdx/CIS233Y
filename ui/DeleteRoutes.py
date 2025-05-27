from ui.WebUI import WebUI
from flask import render_template, request
from logic.GamesLibrary import GamesLibrary
from logic.VideoGame import VideoGame

class DeleteRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route("/delete_video_game")
    def delete_video_game():
        return render_template(
            "delete/delete_video_game.html",
            games=WebUI.get_all_games()
        )

    @staticmethod
    @__app.route("/do_delete_video_game", methods=['GET', 'POST'])
    def do_delete_video_game():
        game_key, error = WebUI.validate_field(object_name="video game", field_name="game")
        if game_key is None:
            return error
        game = VideoGame.lookup(game_key)
        if game is None:
            return render_template(
                "error.html",
                message_header="Game does not exist!",
                message_body=f"The game {game_key} does not exist. Please choose another game and try again."
            )
        for library in WebUI.get_all_libraries():
            if game in library:
                library.remove(game)
        game.delete()
        # when this happens i can no longer pass the variables that identify the game into the HTML. not sure how to fix.
        return render_template("delete/confirm_video_game_deleted.html")

    @staticmethod
    @__app.route("/delete_library")
    def delete_library():
        return render_template(
            "delete/delete_library.html",
            libraries=WebUI.get_all_libraries()
        )

    @staticmethod
    @__app.route("/do_delete_library", methods=["GET", "POST"])
    def do_delete_library():
        library_key, error = WebUI.validate_field(object_name="library", field_name="library")
        if library_key is None:
            return error
        library = GamesLibrary.lookup(library_key.lower())
        if library.get_name() == GamesLibrary.ALL_GAMES:
            return render_template(
                "error.html",
                message_header=f"Cannot delete library.",
                message_body=f"Cannot delete the {GamesLibrary.ALL_GAMES} library."
            )
        if library is None:
            return render_template(
                "error.html",
                message_header=f"Library {library_key} not found.",
                message_body=f"The library {library_key} does not exist. "
                             f"Please choose another library and try again."
            )
        WebUI.get_all_libraries().remove(library)
        library.delete()
        return render_template("delete/confirm_library_deleted.html", library=library)
