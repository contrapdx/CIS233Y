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
            print("Connection to database successful")

    @classmethod
    def rebuild_data(cls):
        cls.connect()

        cls.__games_collection.drop()
        cls.__games_collection = cls.__database.Games
        cls.__libraries_collection.drop()
        cls.__libraries_collection = cls.__database.Libraries
        cls.__users_collection.drop()
        cls.__users_collection = cls.__database.Users

        all_games, all_libraries, all_users = cls.get_data()

        user_dicts = [user.to_dict() for user in all_users]
        cls.__users_collection.insert_many(user_dicts)

        game_dicts = [game.to_dict() for game in all_games]
        cls.__games_collection.insert_many(game_dicts)

        library_dict = [library.to_dict() for library in all_libraries]
        cls.__libraries_collection.insert_many(library_dict)

    @classmethod
    def read_data(cls, user_key):
        cls.connect()
        game_map = {}
        game_dicts = list(cls.__games_collection.find({"user_key": user_key}))
        games = [VideoGame.build(game_dict, game_map) for game_dict in game_dicts]

        library_map = {}
        library_dicts = list(cls.__libraries_collection.find({"user_key": user_key}))
        libraries = [GamesLibrary.build(library_dict, library_map, game_map) for library_dict in library_dicts]

        return library_map[GamesLibrary.make_key(GamesLibrary.ALL_GAMES)], libraries, game_map, library_map

    @classmethod
    def read_user(cls, username):
        cls.connect()
        user_dict = cls.__users_collection.find_one({"_id": username.lower()})
        if user_dict is None:
            return None
        else:
            return User.build(user_dict)

    @classmethod
    def get_data(cls):

        user1 = User("Connor", b'$2b$13$nlDAygkYnq5WdN.Rab/mFe.ylOu8xgfwPwoaEdB.q4EEuU4VL35tW')
        user2 = User("FGC", b'$2b$13$P981uErsdmK1wlsksPRj7OHpSY4aVjzu6hlJX0YpL94r1nckj314G')
        user3 = User("Tester", b'$2b$12$sdEgSknZ1EJfcfBRSi8jbOM9Atgw3mP2h4KUz940gAY5XciZ5whvq')

        game_map = {}
        library_map = {}

        kirby64 = VideoGame(title="Kirby 64: The Crystal Shards",
                            release_year=2000,
                            developer="Nintendo",
                            genre="Action-Platform Game",
                            series="Kirby",
                            game_map=game_map,
                            user_key=user1.get_key())
        lozoot = VideoGame(title="The Legend of Zelda: Ocarina of Time",
                           release_year=1998,
                           developer="Nintendo",
                           genre="Action-Adventure Game",
                           series="The Legend of Zelda",
                            game_map=game_map,
                           user_key=user1.get_key())
        ssb4 = FightingGame(title="Super Smash Bros. for Wii U",
                            release_year=2014,
                            developer="Nintendo",
                            genre="Fighting Game",
                            series="Super Smash Bros.",
                            subgenre="Platform Fighter",
                            shorthand="SSB4",
                            evo_appearances=5,
                            game_map=game_map,
                            user_key=user2.get_key())
        ssbu = FightingGame(title="Super Smash Bros. Ultimate",
                            release_year=2018,
                            developer="Nintendo",
                            genre="Fighting Game",
                            series="Super Smash Bros.",
                            subgenre="Platform Fighter",
                            shorthand="SSBU",
                            evo_appearances=2,
                            game_map=game_map,
                            user_key=user2.get_key())
        ssbm = FightingGame(title="Super Smash Bros. Melee",
                            release_year=2001,
                            developer="Nintendo",
                            genre="Fighting Game",
                            series="Super Smash Bros.",
                            subgenre="Platform Fighter",
                            shorthand="SSBM",
                            evo_appearances=7,
                            game_map=game_map,
                            user_key=user2.get_key())

        gng = VideoGame(title="Ghouls 'n Ghosts",
                        release_year=1988,
                        developer="Capcom",
                        genre="Platformer",
                        series="Ghosts 'n Goblins",
                        game_map=game_map,
                        user_key=user1.get_key())
        re4 = VideoGame(title="Resident Evil 4",
                        release_year=2005,
                        developer="Capcom",
                        genre="Survival Horror Game",
                        series="Resident Evil",
                        game_map=game_map,
                        user_key=user1.get_key())
        sf3s = FightingGame(title="Street Fighter III: 3rd Strike",
                            release_year=1999,
                            developer="Capcom",
                            genre="Fighting Game",
                            series="Street Fighter",
                            subgenre="Traditional Fighter",
                            shorthand="SF3S",
                            evo_appearances=10,
                            game_map=game_map,
                            user_key=user2.get_key())
        sf6 = FightingGame(title="Street Fighter 6",
                           release_year=2023,
                           developer="Capcom",
                           genre="Fighting Game",
                           series="Street Fighter",
                           subgenre="Traditional Fighter",
                           shorthand="SF6",
                           evo_appearances=3,
                           game_map=game_map,
                           user_key=user2.get_key())
        umvc3 = FightingGame(title="Ultimate Marvel vs. Capcom 3",
                             release_year=2011,
                             developer="Capcom",
                             genre="Fighting Game",
                             series="Marvel vs. Capcom",
                             subgenre="Tag Fighter",
                             shorthand="UMVC3",
                             evo_appearances=7,
                             game_map=game_map,
                             user_key=user2.get_key())

        d2lod = VideoGame(title="Diablo II: Lord of Destruction",
                          release_year=2001,
                          developer="Blizzard Entertainment",
                          genre="Action Role Playing Game",
                          series="Diablo",
                          game_map=game_map,
                          user_key=user1.get_key())
        wc3 = VideoGame(title="Warcraft III: Reign of Chaos",
                        release_year=2002,
                        developer="Blizzard Entertainment",
                        genre="Real-Time Strategy Game",
                        series="Warcraft",
                        game_map=game_map,
                        user_key=user1.get_key())
        ow = VideoGame(title="Overwatch",
                       release_year=2016,
                       developer="Blizzard Entertainment",
                       genre="Hero Shooter",
                       series="Overwatch",
                       game_map=game_map,
                       user_key=user1.get_key())

        nintendo = GamesLibrary(name="Nintendo",
                                games=[kirby64, lozoot],
                                icon="https://upload.wikimedia.org/wikipedia/commons/b/b3/Nintendo_red_logo.svg",
                                description="Games developed by Nintendo",
                                library_map=library_map,
                                user_key=user1.get_key())
        capcom = GamesLibrary(name="Capcom",
                              games=[gng, re4],
                              icon="https://upload.wikimedia.org/wikipedia/commons/e/ef/Capcom_logo.svg",
                              description="Games developed by Capcom",
                              library_map=library_map,
                              user_key=user1.get_key())
        blizzard = GamesLibrary(name="Blizzard Entertainment",
                                games=[d2lod, wc3, ow],
                                icon="https://upload.wikimedia.org/wikipedia/commons/b/b2/Blizzard_Entertainment_Logo.svg",
                                description="Games developed by Blizzard Entertainment",
                                library_map=library_map,
                                user_key=user1.get_key())
        evo = GamesLibrary(name="EVO Titles",
                           games=[ssb4, ssbu, ssbm, sf3s, sf6, umvc3],
                           icon="https://upload.wikimedia.org/wikipedia/en/3/36/Evo_Championship_Series_Logo.png",
                           description="Games featured at Evolution Championship Series",
                           library_map=library_map,
                           user_key=user2.get_key())
        u1_all = GamesLibrary(name=GamesLibrary.ALL_GAMES,
                              games=[kirby64, lozoot, gng, re4, d2lod, wc3, ow],
                              icon="https://upload.wikimedia.org/wikipedia/commons/a/a7/Video_game_controller_icon_designed_by_Maico_Amorim.svg",
                              description="All of Connor's Games",
                              library_map=library_map,
                              user_key=user1.get_key())
        u2_all = GamesLibrary(name=GamesLibrary.ALL_GAMES,
                              games=[ssb4, ssbu, ssbm, sf3s, sf6, umvc3],
                              icon="https://upload.wikimedia.org/wikipedia/commons/a/a7/Video_game_controller_icon_designed_by_Maico_Amorim.svg",
                              description="All FGC Games",
                              library_map=library_map,
                              user_key=user2.get_key())
        u3_all = GamesLibrary(name=GamesLibrary.ALL_GAMES,
                              games=[],
                              icon="https://upload.wikimedia.org/wikipedia/commons/a/a7/Video_game_controller_icon_designed_by_Maico_Amorim.svg",
                              description="All Tester Games",
                              library_map=library_map,
                              user_key=user3.get_key())

        return ([kirby64, lozoot, gng, re4, d2lod, wc3, ow, ssb4, ssbu, ssbm, sf3s, sf6, umvc3],
                [nintendo, capcom, blizzard, evo, u1_all, u2_all, u3_all], [user1, user2, user3])

    @classmethod
    def save_library(cls, library):
        cls.connect()
        library_dict = library.to_dict()
        cls.__libraries_collection.update_one({"_id": library_dict["_id"]}, {"$set": library_dict}, upsert=True)

    @classmethod
    def save_game(cls, game):
        cls.connect()
        game_dict = game.to_dict()
        cls.__games_collection.update_one({"_id": game_dict["_id"]}, {"$set": game_dict}, upsert=True)

    @classmethod
    def add_user(cls, user):
        cls.connect()
        user_dict = user.to_dict()
        cls.__users_collection.insert_one(user_dict)

    @classmethod
    def delete_library(cls, library):
        cls.connect()
        cls.__libraries_collection.delete_one({"_id": library.get_id()})

    @classmethod
    def delete_game(cls, game):
        cls.connect()
        cls.__games_collection.delete_one({"_id": game.get_id()})

if __name__ == '__main__':
    Database.connect()
    print(Database.read_user("Test"))
