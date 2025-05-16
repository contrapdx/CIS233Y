from ui.WebUI import WebUI
from flask import render_template, request
from logic.GamesLibrary import GamesLibrary

class CreateRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route('/create_library')
    def create_library():
        return render_template("create/create_library.html")