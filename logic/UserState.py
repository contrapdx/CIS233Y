class UserState:
    __user = None
    __all_games = None
    __all_libraries = None
    __game_map = None
    __library_map = None
    __map = {}

    def __init__(self, user):
        from data.Database import Database

        self.__user = user
        self.__all_games, self.__all_libraries, self.__game_map, self.__library_map = (
            Database.read_data(user.get_key())
        )
        self.__class__.__map[self.get_key()] = self

    @classmethod
    def logout(cls, user_key):
        if user_key in cls.__map:
            del cls.__map[user_key]

    def get_key(self):
        return self.__user.get_key()

    def get_all_libraries(self):
        return self.__all_libraries

    def get_all_games(self):
        return self.__all_games

    def get_library_map(self):
        return self.__library_map

    def get_game_map(self):
        return self.__game_map

    @classmethod
    def lookup(cls, key):
        if key in cls.__map:
            return cls.__map[key]
        else:
            return None

    def lookup_library(self, key):
        if key in self.__library_map:
            return self.__library_map[key]
        return None

    def lookup_game(self, key):
        if key in self.__game_map:
            return self.__game_map[key]
        return None
