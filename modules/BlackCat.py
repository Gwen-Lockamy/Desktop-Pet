from PyQt5.QtGui import QPixmap

class Data:
    def __init__(self):
        self.idle = self.initStateSprites("Idle")
        self.itch = self.initStateSprites("Itch")
        self.lay = self.initStateSprites("Laying")
        self.licking1 = self.initStateSprites("Licking1")
        self.licking2 = self.initStateSprites("Licking2")
        self.meow = self.initStateSprites("Meow")
        self.sitting = self.initStateSprites("Sitting")
        self.sleeping1 = self.initStateSprites("Sleeping1")
        self.sleeping2 = self.initStateSprites("Sleeping2")
        self.stretching = self.initStateSprites("Stretching")
        self.walk = self.initStateSprites("Walk")

    def initStateSprites(self, state_file):
        sheet = QPixmap(f"assets/Black-Cat/{state_file}.png")
        frame_height = sheet.height()
        count = int(sheet.width() / frame_height)
        frame_width = int(sheet.width() / count)

        frames = []
        for i in range(count):
            frame = sheet.copy(i * frame_width, 0, frame_width, frame_height)
            frames.append(frame)
        return frames
