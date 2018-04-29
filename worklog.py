from mainmenu import *
from models import *

if __name__ == "__main__":
    # initialize the database, if setup already it will use existing
    initialize()
    main_menu = MainMenu()
    main_menu.menu_loop()
