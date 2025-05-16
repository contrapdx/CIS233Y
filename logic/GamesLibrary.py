class GamesLibrary:
    __name = ""
    __games = []
    __icon = ""
    __description = ""
    __map = {}

    ALL_GAMES = "All Games"

    def __init__(self, name, games, icon, description, save=False):
        self.__name = name
        self.__games = games
        self.__icon = icon
        self.__description = description
        self.__class__.__map[self.get_key()] = self
        if save:
            self.save()

    @classmethod
    def build(cls, library_dict):
        from logic.VideoGame import VideoGame
        return GamesLibrary(
            library_dict["name"],
            [VideoGame.lookup(key) for key in library_dict["games"]],
            library_dict["icon"],
            library_dict["description"]
        )

    def to_dict(self):
        return {
            "_id": self.get_key(),
            "name": self.__name,
            "icon": self.__icon,
            "description": self.__description,
            "games": [game.get_key() for game in self.__games]
        }

    def get_key(self):
        return self.__name.lower()

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_icon(self):
        return self.__icon

    @classmethod
    def lookup(cls, key):
        lower_key = key.lower()
        if lower_key in cls.__map:
            return cls.__map[lower_key]
        else:
            return None

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
        del self.__class__.__map[self.get_key()]
        Database.delete_library(self)

    def __iter__(self):
        return self.__games.__iter__()

    def __contains__(self, game):
        return game in self.__games

    def __add__(self, other):
        name = f"{self.get_name()} / {other.get_name()}"
        icon = f"{self.get_icon()} / {other.get_icon()}"
        description = self.get_description() + ", and " + other.get_description()
        new_library = GamesLibrary(name, [], icon, description, save=True)
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
