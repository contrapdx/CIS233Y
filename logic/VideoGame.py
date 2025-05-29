class VideoGame:
    __title = ""
    __release_year = 0
    __developer = ""
    __genre = ""
    __series = ""
    __user_key = ""

    def __init__(self, title, release_year, developer, genre, series, user_key, game_map, save=False):
        self.__title = title
        self.__release_year = release_year
        self.__developer = developer
        self.__genre = genre
        self.__series = series
        self.__user_key = user_key
        game_map[self.get_key()] = self
        if save:
            self.save()

    @classmethod
    def build(cls, game_dict, game_map):
        from logic.FightingGame import FightingGame
        if game_dict["type"] == "Video Game":
            return VideoGame(
                game_dict["title"],
                game_dict["release_year"],
                game_dict["developer"],
                game_dict["genre"],
                game_dict["series"],
                game_dict["user_key"],
                game_map
            )
        elif game_dict["type"] == "Fighting Game":
            return FightingGame(
                game_dict["title"],
                game_dict["release_year"],
                game_dict["developer"],
                game_dict["genre"],
                game_dict["series"],
                game_dict["user_key"],
                game_map,
                game_dict["subgenre"],
                game_dict["shorthand"],
                game_dict["evo_appearances"]
            )

    def to_dict(self):
        return {
            "_id": f"{self.get_key()}|{self.__user_key}",
            "type": "Video Game",
            "title": self.__title,
            "release_year": self.__release_year,
            "developer": self.__developer,
            "genre": self.__genre,
            "series": self.__series,
            "user_key": self.__user_key
        }

    def get_key(self):
        return f"{self.__title} ({self.__release_year})".lower()

    def get_printable_key(self):
        return f"{self.__title} ({self.__release_year})"

    def get_id(self):
        return f"{self.get_key()}|{self.__user_key}"

    @staticmethod
    def make_key(title, release_year):
        return f"{title} ({release_year})".lower()

    def get_title(self):
        return self.__title

    def get_release_year(self):
        return self.__release_year

    def get_developer(self):
        return self.__developer

    def get_genre(self):
        return self.__genre

    def get_series(self):
        return self.__series

    def update_series(self, series):
        self.__series = series
        self.save()

    def delete(self):
        from data.Database import Database
        from logic.UserState import UserState

        game_key = self.get_key()
        user_state = UserState.lookup(self.__user_key)
        game_map = user_state.get_game_map()
        if game_key in game_map:
            del game_map[game_key]
        Database.delete_game(self)

    def __str__(self):
        return (f"{self.__title} ({self.__release_year}). "
                f"{self.__genre} developed by {self.__developer}. ")

    def save(self):
        from data.Database import Database
        Database.save_game(self)
