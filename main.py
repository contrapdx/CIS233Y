from ui.WebUI import WebUI
from logic.GamesLibrary import GamesLibrary
from data.Database import Database

if __name__ == '__main__':
    #GamesLibrary.rebuild_data() # rebuild_database.py wasn't seeing the "logic" folder for some reason.
    WebUI.init()
    WebUI.run()
