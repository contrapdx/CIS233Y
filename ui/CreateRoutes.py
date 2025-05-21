from ui.WebUI import WebUI
from flask import render_template, request
from logic.GamesLibrary import GamesLibrary
from logic.VideoGame import VideoGame

class CreateRoutes(WebUI):
    __app = WebUI.get_app()

    @staticmethod
    @__app.route('/create_library')
    def create_library():
        return render_template("create/create_library.html")

    @staticmethod
    @__app.route('/do_create_library', methods=['GET', 'POST'])
    def do_create_library():
        name, error = WebUI.validate_field("name")
        if name is None:
            return error
        key = name.lower()
        library = GamesLibrary.lookup(key)
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
        library = GamesLibrary(name=name, games=[], icon=icon, description=description, save=True)
        WebUI.get_all_libraries().append(library)
        return render_template("create/confirm_library_created.html", library=library)

    @staticmethod
    @__app.route('/create_video_game')
    def create_video_game():
        return render_template("create/create_video_game.html")

    @staticmethod
    @__app.route('/do_create_video_game', methods=['GET', 'POST'])
    def do_create_video_game():
        # title, release_year, developer, genre, series
        title, error = WebUI.validate_field("title")
        if title is None:
            return error
        release_year, error = WebUI.validate_field("release_year")
        if release_year is None:
            return error
        key = VideoGame.make_key(title, release_year).lower()
        game = VideoGame.lookup(key)
        if game is not None:
            return render_template(
                "error.html",
                message_header="Game already exists!",
                message_body=f"The game '{title} ({release_year})' already exists. Please choose another game and try again."
            )
        developer, error = WebUI.validate_field("developer")
        if developer is None:
            return error
        genre, error = WebUI.validate_field("genre")
        if genre is None:
            return error
        if "series" in request.form:
            series = request.form["series"].strip()
        else:
            series = ""
        game = VideoGame(title, release_year, developer, genre, series, save=True)
        WebUI.get_all_games().append(game)
        return render_template("create/confirm_video_game_created.html", game=game)
