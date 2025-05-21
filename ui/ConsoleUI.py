import ui.input_validation as v
from logic.GamesLibrary import GamesLibrary
from logic.VideoGame import VideoGame
from logic.FightingGame import FightingGame

class ConsoleUI:
    __all_games = None
    __all_libraries = []

    CHOICES = {
        "l": "list", "list": "list",
        "plib":"print libraries", "print libraries":"print libraries",
        "clib":"create library", "create library":"create library",
        "dlib":"delete library", "delete library":"delete library",
        "slib":"show library", "show library":"show library",
        "cg":"create game", "create game":"create game",
        "ag":"add game to library", "add game to library":"add game to library",
        "rg":"remove game from library", "remove game from library":"remove game from library",
        "ug":"update game info", "update game info":"update game info",
        "dg":"delete game", "delete game":"delete game",
        "jlib":"join libraries", "join libraries":"join libraries",
        "x": "exit", "exit":"exit"
    }

    @classmethod
    def init(cls):
        cls.__all_games, cls.__all_libraries = GamesLibrary.read_data()

    @classmethod
    def select_game(cls, library=None):
        if library is None:
            library = cls.__all_games
        keys = []
        map = {}
        pos = 1
        for game in library:
            keys.append(game.get_key())
            map[str(pos)] = game.get_key()
            pos += 1
        keys.append("None")
        map[str(pos)] = "None"
        print("List of games: ")
        pos = 1
        for key in keys:
            print(f"    {pos}: {key}")
            pos += 1
        key = v.select_item(prompt="Please select a game, or 'None' to exit: ",
                            error="Invalid selection: Game must exist.",
                            options=keys, map=map)
        if key == "None":
            return None
        game = VideoGame.lookup(key)
        return game

    @classmethod
    def select_library(cls, include_all=False):
        names = []
        map = {}
        pos = 1
        for library in cls.__all_libraries:
            if include_all or library.get_name() != GamesLibrary.ALL_GAMES:
                names.append(library.get_name())
                map[str(pos)] = library.get_name()
                pos += 1
        names.append("None")
        map[str(pos)] = "None"
        print("List of libraries: ")
        pos = 1
        for name in names:
            print(f"    {pos}: {name}")
            pos += 1
        name = v.select_item(prompt="Please select a library, or 'None' to exit: ",
                             error="Invalid selection: Library must exist.",
                             options=names, map=map)
        if name == "None":
            return None
        library = GamesLibrary.lookup(name)
        return library

    @classmethod
    def list_video_games(cls):
        for game in cls.__all_games:
            print(game.get_key(), ": ", game, sep="")
        print("")

    @classmethod
    def list_libraries(cls):
        for library in cls.__all_libraries:
            print(f"{library.get_name()}: {library.get_description()}")
        print("")

    @classmethod
    def create_library(cls):
        name = v.input_string(prompt="Please enter the name of the game library, or 'None' to exit: ",
                              error="Name must be non-empty.")
        if name == "None":
            return
        library = GamesLibrary.lookup(name)
        if library is not None:
            print("Error! Library with that name already exists.")
            return
        icon = v.input_string(prompt="Please input the URL to the icon image: ", error="URL must be non-empty.")
        description = v.input_string(prompt="Please enter a description for the library: ", valid=lambda x: True)
        library = GamesLibrary(name=name, games=[], icon=icon, description=description, save=True)
        cls.__all_libraries.append(library)
        print(f"Library '{name}' created successfully.")

    @classmethod
    def delete_library(cls):
        library = cls.select_library()
        if library is None:
            return
        cls.__all_libraries.remove(library)
        library.delete()
        print(f"Deleted successfully.")

    @classmethod
    def show_library(cls):
        library = cls.select_library(True)
        if library is None:
            return
        print("")
        print(f"Name: {library.get_name()}")
        print(f"Description: {library.get_description()}")
        print(f"Icon: {library.get_icon()}")
        print(f"Games in library: ")
        for game in library:
            print("    -", game)
        print("")

    @classmethod
    def join_libraries(cls):
        library_1 = cls.select_library(include_all=True)
        library_2 = cls.select_library(include_all=True)
        if library_1 is None or library_2 is None:
            return
        new_library = library_1 + library_2
        cls.__all_libraries.append(new_library)
        print(f"Joined {library_1} and {library_2} libraries successfully.")

    @classmethod
    def create_game(cls):
        fgc_check = v.y_or_n(prompt="Is this game a fighting game (y/n): ")
        title = v.input_string(prompt="Please enter the title of the game: ")
        release_year = v.input_int(prompt="Please enter the release year of the game: ",
                                   error="Invalid release year: Must be between 1950 and 2030.",
                                   ge=1950, le=2030)

        if not fgc_check:
            key = VideoGame.make_key(title, release_year)
            game = VideoGame.lookup(key)
            if game is not None:
                print("Game already exists.")
                return
        if fgc_check:
            shorthand = v.input_string(prompt="Please enter the shorthand of the game: ")
            key = FightingGame.make_key(title, shorthand)
            game = FightingGame.lookup(key)
            if game is not None:
                print("Game already exists.")
                return

        developer = v.input_string(prompt="Please enter the developer of the game: ")
        genre = v.input_string(prompt="Please enter the genre of the game: ")
        series = v.input_string(prompt="Please enter the series of the game (can be empty): ", valid=lambda x: True)
        if fgc_check:
            subgenre = v.input_string(prompt="Please enter the subgenre of fighting game: ")
            evo_appearances = v.input_int(prompt="Please enter the number of EVO appearances this game has: ",
                                          ge=0, le=20)
            game = FightingGame(title=title, release_year=release_year, developer=developer, genre=genre,
                                series=series, subgenre=subgenre, shorthand=shorthand, evo_appearances=evo_appearances,
                                save=True)
        else:
            game = VideoGame(title=title, release_year=release_year, developer=developer, genre=genre,
                             series=series, save=True)
        cls.__all_games.append(game)
        print(f"{key} created successfully.")

    @classmethod
    def add_game(cls):
        library = cls.select_library()
        if library is None:
            return
        game = cls.select_game()
        if game is None:
            return
        if game in library:
            print("Game already in library.")
            return
        library.append(game)
        print(f"Game added to library.")

    @classmethod
    def remove_game(cls):
        library = cls.select_library()
        if library is None:
            return
        game = cls.select_game(library)
        if game is None:
            return
        if game not in library:
            print("The game is not in that library.")
            return
        library.remove(game)
        print("Removed game from library.")

    @classmethod
    def update_game(cls):
        game = cls.select_game()
        if game is None:
            return
        series = v.input_string(prompt="Please enter the series the game belongs to (can be empty): ",
                                valid=lambda x: True)
        game.update_series(series)
        print(f"Game updated successfully.")

    @classmethod
    def delete_game(cls):
        game = cls.select_game()
        if game is None:
            return
        for library in cls.__all_libraries:
            if game in library:
                library.remove(game)
        game.delete()
        print(f"Game deleted successfully.")

    @classmethod
    def run(cls):
        while True:
            cls.print_menu()
            choice = v.select_item("Please select an option: ", "Selection must be a valid choice.",
                                   map=cls.CHOICES)
            print("")
            if choice == "exit":
                print("Goodbye!")
                break
            elif choice == "list":
                cls.list_video_games()
            elif choice == "print libraries":
                cls.list_libraries()
            elif choice == "create library":
                cls.create_library()
            elif choice == "delete library":
                cls.delete_library()
            elif choice == "show library":
                cls.show_library()
            elif choice == "create game":
                cls.create_game()
            elif choice == "add game to library":
                cls.add_game()
            elif choice == "remove game from library":
                cls.remove_game()
            elif choice == "update game info":
                cls.update_game()
            elif choice == "join libraries":
                cls.join_libraries()
            elif choice == "delete game":
                cls.delete_game()

    @staticmethod
    def print_menu():
        print("Selection options: ")
        print("     l: Print all games")
        print("     plib: Print all libraries")
        print("     clib: Create a library")
        print("     dlib: Delete a library")
        print("     slib: Show contents of a library")
        print("     jlib: Join/combine two libraries")
        print("     cg: Create a game")
        print("     dg: Delete a game")
        print("     ag: Add game to library")
        print("     rg: Remove game from library")
        print("     ug: Update game series")
        print("     x: Exit")

if __name__ == '__main__':
    ConsoleUI.init()
    ConsoleUI.run()
