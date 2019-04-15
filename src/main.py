import sys
from PyQt5.QtWidgets import QApplication

from gui import GUI
from labyrinthworld import LabyrinthWorld
from player import Player
from coordinates import Coordinates

def main():
    test_world = LabyrinthWorld(49, 49, 10)
    test_world.set_player(Player("Name_example", test_world))
    test_world.get_player().set_location(Coordinates(0,0))

    app = QApplication(sys.argv)
    gui = GUI(test_world)
    gui.show()

    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()