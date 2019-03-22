import sys
from PyQt5.QtWidgets import QApplication

from gui import GUI
from labyrinthworld import LabyrinthWorld
from player import Player

def main():
    test_world = LabyrinthWorld(49, 49)
    test_world.set_player(Player("Name_example", test_world))
    test_world.read_labyrinth_mapFolder("laby_49x49.txt")

    app = QApplication(sys.argv)
    gui = GUI(test_world, 10)
    gui.show()

    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()