from logic.GamesLibrary import GamesLibrary

if __name__ == '__main__':
    all_games, all_libraries = GamesLibrary.read_data()
    print()
    print("All Games: ")
    for game in all_games:
        print(game)
    print()
    print("All Libraries: ")
    for library in all_libraries:
        print(library)
