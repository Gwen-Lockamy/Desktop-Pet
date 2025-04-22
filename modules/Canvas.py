from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon 
from PyQt5.QtCore import Qt 
from screeninfo import get_monitors 
from .Companion import *

class Window(QMainWindow):
    def __init__(self): 
        super().__init__()
        self.monitor = get_monitors()[0] 
        self.size = 150
        self.icon = QIcon(("assets/icon.jpg"))

        # Init Window
        self.setGeometry(0, 0, self.monitor.width, self.monitor.height)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("Desktop Pet: " + name)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: transparent;")
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.initTray()
        self.initPet()
    
    def initTray(self):
        tray_icon = QSystemTrayIcon(self)
        tray_icon.setIcon(self.icon)

        tray_menu = QMenu()
        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(QApplication.quit)
        tray_menu.addAction(quit_action)

        tray_icon.setContextMenu(tray_menu)
        tray_icon.show()

    def initPet(self):
        self.pet = Pet(self)
        self.label = QLabel(self)
        self.label.setPixmap(self.pet.data.idle[0])
        self.label.setGeometry(   
            int(self.monitor.width * 0.60), 
            int(self.monitor.height * 0.91),
            self.size, 
            self.size
        )
        self.label.setScaledContents(True)
        self.label.show()
        self.animatePet(self.pet)

    def animatePet(self, pet):
        self.timer = QTimer()
        self.timer.timeout.connect(pet.animate)
        self.timer.start(200)

    
    
