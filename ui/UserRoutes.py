from ui.WebUI import WebUI
from flask import render_template, request, session
from logic.GamesLibrary import GamesLibrary
from logic.VideoGame import VideoGame
from logic.FightingGame import FightingGame

class UserRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route("/get_user")
    def get_user():
        if "username" in session:
            return session["username"]
        return "None"

    @staticmethod
    @__app.route("/set_user")
    def set_user():
        if "username" in request.args:
            session["username"] = request.args["username"]
            return "User set."
        if "username" in session:
            del session["username"]
        return "User cleared."
