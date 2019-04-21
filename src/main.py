import sys
from PyQt5.QtWidgets import QApplication

from gui import GUI
from labyrinthworld import LabyrinthWorld

def main():
    
    test_world = LabyrinthWorld()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    gui = GUI(test_world)

    sys.exit(app.exec_())
    
    
if __name__ == "__main__":
    main()