class GamesLibrary:
    __name = ""
    __games = []
    __icon = ""
    __description = ""
    __user_key = ""

    ALL_GAMES = "All Games"

    def __init__(self, name, games, icon, description, user_key, library_map, save=False):
        self.__name = name
        self.__games = games
        self.__icon = icon
        self.__description = description
        self.__user_key = user_key
        library_map[self.get_key()] = self
        if save:
            self.save()

    @classmethod
    def build(cls, library_dict, library_map, game_map):
        from logic.VideoGame import VideoGame

        return GamesLibrary(
            library_dict["name"],
            [game_map[key] for key in library_dict["games"]],
            library_dict["icon"],
            library_dict["description"],
            library_dict["user_key"],
            library_map
        )

    def to_dict(self):
        return {
            "_id": self.get_id(),
            "name": self.__name,
            "icon": self.__icon,
            "description": self.__description,
            "user_key": self.__user_key,
            "games": [game.get_key() for game in self.__games]
        }

    def get_key(self):
        return self.__name.lower()

    def get_id(self):
        return f"{self.get_key()}|{self.__user_key}"

    @staticmethod
    def make_key(name):
        return name.lower()

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_icon(self):
        return self.__icon

    def append(self, game, save=True):
        from data.Database import Database
        self.__games.append(game)
        if save:
            Database.save_library(self)

    def remove(self, game):
        from data.Database import Database
        self.__games.remove(game)
        Database.save_library(self)

    def delete(self):
        from data.Database import Database
        from logic.UserState import UserState

        library_key = self.get_key()
        user_state = UserState.lookup(self.__user_key)
        library_map = user_state.get_library_map()
        if library_key in library_map:
            del library_map[library_key]
        Database.delete_library(self)

    def __iter__(self):
        return self.__games.__iter__()

    def __contains__(self, game):
        return game in self.__games

    def __add__(self, other):
        from logic.UserState import UserState
        name = f"{self.get_name()} / {other.get_name()}"
        icon = f"{self.get_icon()} / {other.get_icon()}"
        description = self.get_description() + ", and " + other.get_description()
        user_key = self.__user_key
        user_state = UserState.lookup(user_key)
        new_library = GamesLibrary(name, [], icon, description,
                                   user_key, user_state.get_library_map(), save=True)
        for game in self:
            if game not in new_library:
                new_library.append(game, save=False)
        for game in other:
            if game not in new_library:
                new_library.append(game, save=False)
        new_library.save()
        return new_library

    def __str__(self):
       s = (f"{self.__name} Library: {self.__description}\n"
                f"Icon: {self.__icon}\n"
                f"Contents: \n")
       pos = 1
       for game in self.__games:
           s += f"    {pos}: {game}\n"
           pos += 1
       return s

    @staticmethod
    def get_games_library():
        from data.Database import Database
        return Database.get_data()

    @staticmethod
    def rebuild_data():
        from data.Database import Database
        return Database.rebuild_data()

    @staticmethod
    def read_data():
        from data.Database import Database
        return Database.read_data()

    def save(self):
        from data.Database import Database
        Database.save_library(self)
