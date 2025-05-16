from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from logic.GamesLibrary import GamesLibrary
from logic.VideoGame import VideoGame
from logic.FightingGame import FightingGame

class Database:
    USERNAME = "GameLibraryManager"
    PASSWORD = "sLwGhOBf3Md2a5Kx"
    CLUSTER = "cluster0.ohrbxuc.mongodb.net"
    __connection = None
    __database = None
    __games_collection = None
    __libraries_collection = None
    URI = f"mongodb+srv://{USERNAME}:{PASSWORD}@{CLUSTER}/?retryWrites=true&w=majority&appName=Cluster0"

    @classmethod
    def connect(cls):
        if cls.__connection is None:
            cls.__connection = MongoClient(cls.URI, server_api=ServerApi('1'))
            cls.__database = cls.__connection.GameBox
            cls.__games_collection = cls.__database.Games
            cls.__libraries_collection = cls.__database.Libraries
            print("Connection successful")

    @classmethod
    def rebuild_data(cls):
        cls.connect()

        # Remake both collections
        cls.__games_collection.drop()
        cls.__games_collection = cls.__database.Games
        cls.__libraries_collection.drop()
        cls.__libraries_collection = cls.__database.Libraries

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
                                icon="https://cdn.discordapp.com/attachments/1356380380034498823/1373045180604743801/lxEd50b.png?ex=6828fb79&is=6827a9f9&hm=079107d727657f740107623fa00c4379c8e0c508464cb78b0b7267e2d8b9fb25&",
                                description="Games developed by Nintendo")
        capcom = GamesLibrary(name="Capcom", games=[gng, re4, sf3s, sf6, umvc3],
                              icon="https://cdn.discordapp.com/attachments/1356380380034498823/1373045153119604897/Wa5rE99.png?ex=6828fb72&is=6827a9f2&hm=423cf9dbf060e2c2ef2852544879423adba13690afbf5620c23758a7340203cd&",
                              description="Games developed by Capcom")
        blizzard = GamesLibrary(name="Blizzard Entertainment", games=[d2lod, wc3, ow],
                                icon="https://cdn.discordapp.com/attachments/1356380380034498823/1373044700973633566/XzQAoZS.png?ex=6828fb06&is=6827a986&hm=f72b5f28d65ce40f9b507e1e0cf01e1492827b67df9b7542bd4eabf793fa5419&",
                                description="Games developed by Blizzard Entertainment")
        evo = GamesLibrary(name="EVO Titles", games=[ssb4, ssbu, ssbm, sf3s, sf6, umvc3],
                           icon="https://cdn.discordapp.com/attachments/1356380380034498823/1373045205112197281/3WMuac6.png?ex=6828fb7e&is=6827a9fe&hm=be9c30e3691c73f18ba67e14dd0e260339ba703e488e1501e5ff8c4ed918b9c2&",
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
