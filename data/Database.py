from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from logic.GamesLibrary import GamesLibrary
from logic.VideoGame import VideoGame
from logic.FightingGame import FightingGame
from logic.User import User
from configparser import ConfigParser
import os

class Database:
    __connection = None
    __database = None
    __games_collection = None
    __libraries_collection = None
    __users_collection = None
    APP_NAME = "game_box"

    @classmethod
    def connect(cls):
        if cls.__connection is None:
            if "APPDATA" in os.environ:
                path = f"{os.environ['APPDATA']}\\{cls.APP_NAME}\\{cls.APP_NAME}.ini.txt"
            elif "HOME" in os.environ:
                path = f"{os.environ['HOME']}/.{cls.APP_NAME}/{cls.APP_NAME}.ini.txt"
            else:
                raise Exception("Couldn't find config directory.")
            config_parser = ConfigParser()
            config_parser.read(path)
            username = config_parser["Database"]["username"]
            password = config_parser["Database"]["password"]
            cluster = config_parser["Database"]["cluster"]

            uri = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName=Cluster0"

            cls.__connection = MongoClient(uri, server_api=ServerApi('1'))
            cls.__database = cls.__connection.GameBox
            cls.__games_collection = cls.__database.Games
            cls.__libraries_collection = cls.__database.Libraries
            cls.__users_collection = cls.__database.Users
            print("Connection successful")

    @classmethod
    def rebuild_data(cls):
        cls.connect()

        # Remake both collections
        cls.__games_collection.drop()
        cls.__games_collection = cls.__database.Games
        cls.__libraries_collection.drop()
        cls.__libraries_collection = cls.__database.Libraries
        cls.__users_collection.drop()
        cls.__users_collection = cls.__database.Users

        user1 = User("Connor", b'$2b$13$nlDAygkYnq5WdN.Rab/mFe.ylOu8xgfwPwoaEdB.q4EEuU4VL35tW')
        user2 = User("Not Connor", b'$2b$13$P981uErsdmK1wlsksPRj7OHpSY4aVjzu6hlJX0YpL94r1nckj314G')

        user_dicts = [user.to_dict() for user in [user1, user2]]

        cls.__users_collection.insert_many(user_dicts)
        all_games, all_libraries = cls.get_data()

        game_dicts = [game.to_dict() for game in all_games]
        cls.__games_collection.insert_many(game_dicts)

        library_dict = [library.to_dict() for library in all_libraries]
        cls.__libraries_collection.insert_many(library_dict)

    @classmethod
    def read_data(cls):
        cls.connect()
        game_dicts = list(cls.__games_collection.find())
        games = [VideoGame.build(game_dict) for game_dict in game_dicts]
        library_dicts = list(cls.__libraries_collection.find())
        libraries = [GamesLibrary.build(library_dict) for library_dict in library_dicts]

        return GamesLibrary.lookup(GamesLibrary.ALL_GAMES), libraries

    @classmethod
    def read_user(cls, username):
        user_dict = cls.__users_collection.find_one({"_id": username.lower()})
        if user_dict is None:
            return None
        else:
            return User.build(user_dict)

    @classmethod
    def get_data(cls):

        kirby64 = VideoGame(title="Kirby 64: The Crystal Shards", release_year=2000, developer="Nintendo",
                            genre="Action-Platform Game", series="Kirby")
        lozoot = VideoGame(title="The Legend of Zelda: Ocarina of Time", release_year=1998, developer="Nintendo",
                           genre="Action-Adventure Game", series="The Legend of Zelda")
        ssb4 = FightingGame(title="Super Smash Bros. for Wii U", release_year=2014, developer="Nintendo",
                            genre="Fighting Game", series="Super Smash Bros.", subgenre="Platform Fighter",
                            shorthand="SSB4", evo_appearances=5)
        ssbu = FightingGame(title="Super Smash Bros. Ultimate", release_year=2018, developer="Nintendo",
                            genre="Fighting Game", series="Super Smash Bros.", subgenre="Platform Fighter",
                            shorthand="SSBU", evo_appearances=2)
        ssbm = FightingGame(title="Super Smash Bros. Melee", release_year=2001, developer="Nintendo",
                            genre="Fighting Game", series="Super Smash Bros.", subgenre="Platform Fighter",
                            shorthand="SSBM", evo_appearances=7)

        gng = VideoGame(title="Ghouls 'n Ghosts", release_year=1988, developer="Capcom", genre="Platformer",
                        series="Ghosts 'n Goblins")
        re4 = VideoGame(title="Resident Evil 4", release_year=2005, developer="Capcom",
                        genre="Survival Horror Game", series="Resident Evil")
        sf3s = FightingGame(title="Street Fighter III: 3rd Strike", release_year=1999, developer="Capcom",
                            genre="Fighting Game", series="Street Fighter", subgenre="Traditional Fighter",
                            shorthand="SF3S", evo_appearances=10)
        sf6 = FightingGame(title="Street Fighter 6", release_year=2023, developer="Capcom", genre="Fighting Game",
                           series="Street Fighter", subgenre="Traditional Fighter", shorthand="SF6",
                           evo_appearances=3)
        umvc3 = FightingGame(title="Ultimate Marvel vs. Capcom 3", release_year=2011, developer="Capcom",
                             genre="Fighting Game", series="Marvel vs. Capcom", subgenre="Tag Fighter",
                             shorthand="UMVC3", evo_appearances=7)


        d2lod = VideoGame(title="Diablo II: Lord of Destruction", release_year=2001, developer="Blizzard Entertainment",
                          genre="Action Role Playing Game", series="Diablo")
        wc3 = VideoGame(title="Warcraft III: Reign of Chaos", release_year=2002, developer="Blizzard Entertainment",
                        genre="Real-Time Strategy Game", series="Warcraft")
        ow = VideoGame(title="Overwatch", release_year=2016, developer="Blizzard Entertainment",
                       genre="Hero Shooter", series="Overwatch")

        nintendo = GamesLibrary(name="Nintendo", games=[kirby64, lozoot, ssb4, ssbu, ssbm],
                                icon="https://upload.wikimedia.org/wikipedia/commons/b/b3/Nintendo_red_logo.svg",
                                description="Games developed by Nintendo")
        capcom = GamesLibrary(name="Capcom", games=[gng, re4, sf3s, sf6, umvc3],
                              icon="https://upload.wikimedia.org/wikipedia/commons/e/ef/Capcom_logo.svg",
                              description="Games developed by Capcom")
        blizzard = GamesLibrary(name="Blizzard Entertainment", games=[d2lod, wc3, ow],
                                icon="https://upload.wikimedia.org/wikipedia/commons/b/b2/Blizzard_Entertainment_Logo.svg",
                                description="Games developed by Blizzard Entertainment")
        evo = GamesLibrary(name="EVO Titles", games=[ssb4, ssbu, ssbm, sf3s, sf6, umvc3],
                           icon="https://en.wikipedia.org/wiki/File:Evo_Championship_Series_Logo.png#/media/File:Evo_Championship_Series_Logo.png",
                           description="Games featured at Evolution Championship Series")
        all = GamesLibrary(GamesLibrary.ALL_GAMES, games=[kirby64, lozoot, ssb4, ssbu, ssbm, gng, re4, sf3s,
                                                    sf6, umvc3, d2lod, wc3, ow],
                           icon="", description="All Games")

        return all, [nintendo, capcom, blizzard, evo, all]

    @classmethod
    def save_library(cls, library):
        cls.connect()
        cls.__libraries_collection.update_one({"_id": library.get_key()}, {"$set": library.to_dict()}, upsert=True)

    @classmethod
    def save_game(cls, game):
        cls.connect()
        cls.__games_collection.update_one({"_id": game.get_key()}, {"$set": game.to_dict()}, upsert=True)

    @classmethod
    def delete_library(cls, library):
        cls.connect()
        cls.__libraries_collection.delete_one({"_id": library.get_key()})

    @classmethod
    def delete_game(cls, game):
        cls.connect()
        cls.__games_collection.delete_one({"_id": game.get_key()})

if __name__ == '__main__':
    Database.connect()
    print(Database.read_user("Test"))
