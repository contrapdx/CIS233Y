from ui.WebUI import WebUI
from flask import render_template, request, session, redirect, url_for
from logic.GamesLibrary import GamesLibrary
from logic.VideoGame import VideoGame
from logic.FightingGame import FightingGame
from logic.User import User


class UserRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route("/login")
    def login():
        return render_template("user/login.html")

    @staticmethod
    @__app.route("/do_login", methods=["GET", "POST"])
    def do_login():
        username, error = WebUI.validate_field(object_name="username", field_name="username")
        if error is not None:
            return error
        password, error = WebUI.validate_field(object_name="password", field_name="password")
        if error is not None:
            return error
        type, error = WebUI.validate_field(object_name="type", field_name="type")
        if error is not None:
            return error
        user = User.read_user(username)
        if type == "login":
            if user is None:
                return render_template(
                    "error.html",
                    message_header="Login Failed",
                    message_body="The login attempt was unsuccessful. Please check your account information and try again."
                )
            logged_in = user.verify_password(password)
            if not logged_in:
                return render_template(
                    "error.html",
                    message_header="Login Failed",
                    message_body="The login attempt was unsuccessful. Please check your account information and try again."
                )
            WebUI.login(user)
            return redirect(url_for("homepage"))
        elif type == "register":
            user = User(username, User.hash_password(password))
            user.add()
            all_games = GamesLibrary(
                name=GamesLibrary.ALL_GAMES,
                games=[],
                icon="https://upload.wikimedia.org/wikipedia/commons/a/a7/Video_game_controller_icon_designed_by_Maico_Amorim.svg",
                description=f"All games for {username}",
                user_key=user.get_key(),
                library_map={},
                save=True
            )
            WebUI.login(user)
            return redirect(url_for("homepage"))
        else:
            return render_template(
                "error.html",
                message_header="Unknown login type",
                message_body="Login type must be 'login' or 'register'. I'm not sure how you even got here!"
            )

    @staticmethod
    @__app.route("/logout")
    def logout():
        if "user" in session:
            WebUI.logout()
            del session["user"]
        return redirect(url_for("login"))