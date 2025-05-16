from logic.VideoGame import VideoGame

class FightingGame(VideoGame):
    __subgenre = ""  # airdasher, tag fighter, 3d, platform, etc
    __shorthand = ""  # the fighting game community (fgc) loves using shorthand "codenames"
    __evo_appearances = 0  # evo is the premier fighting game event each year, featuring 8 or 9 main games (usually)
    __map = {}

    def __init__(self, title, release_year, developer, genre, series,
                 subgenre, shorthand, evo_appearances, save=False):
        self.__subgenre = subgenre
        self.__shorthand = shorthand
        self.__evo_appearances = evo_appearances
        super().__init__(title, release_year, developer, genre, series, save=save)
        self.__class__.__map[self.get_key()] = self

    def to_dict(self):
        dict = super().to_dict()
        dict["type"] = "Fighting Game"
        dict["subgenre"] = self.__subgenre
        dict["shorthand"] = self.__shorthand
        dict["evo_appearances"] = self.__evo_appearances
        return dict

    def get_key(self):
        return f"{VideoGame.get_title(self)} ({self.__shorthand})".lower()

    @staticmethod
    def make_key(title, shorthand):
        return f"{title} ({shorthand})".lower()

    def get_subgenre(self):
        return self.__subgenre

    def get_shorthand(self):
        return self.__shorthand

    def get_evo_appearances(self):
        return self.__evo_appearances

    @classmethod
    def lookup(cls, key):
        if key in cls.__map:
            return cls.__map[key]
        else:
            return None

    def __str__(self):
        return (f"{VideoGame.get_title(self)} ({self.__shorthand}). "
                f"{self.__subgenre} developed by {VideoGame.get_developer(self)} "
                f"with {self.__evo_appearances} appearances at EVO. ")
