import random
from PyQt5.QtCore import QTimer, QPoint, Qt, QUrl
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtGui import QTransform
from .BlackCat import Data

name = "Kitty"

class Pet():
    def __init__(self, parent):
        # Data
        self.data = Data()
        self.current_frame = 0
        self.state = "idle"
        self.parent = parent
        # Position Data
        self.direction = -1
        self.position = QPoint(
            int(self.parent.monitor.width * 0.60),
            int(self.parent.monitor.height * 0.91)
        ) 
        # Walk - Sound
        self.walk_sound = QSoundEffect()
        self.walk_sound.setSource(QUrl.fromLocalFile("assets/walk2.wav"))
        self.walk_sound.setLoopCount(QSoundEffect.Infinite)
        self.walk_sound.setVolume(0.05) 
        # Meow - Sound
        self.meow_sound = QSoundEffect()
        self.meow_sound.setSource(QUrl.fromLocalFile("assets/meow.wav"))
        self.meow_sound.setVolume(0.05) 
        # Animation
        self.frame_data = getattr(self.data, self.state)
        self.timer = QTimer()
        self.timer.timeout.connect(self.transitionState)
        self.timer.start(self.duration())
 
    def duration(self):
        if self.state == "meow":
            return 1000
        elif self.state == "lay":
            return 1400
        elif self.state == "stretching":
            return 2600
        elif self.state == "sleeping1" or "sleeping2":
            return random.randint(5000,8000)
        else:
            return random.randint(3000,5000)
    
    def setState(self, new_state):
        if hasattr(self.data, new_state):
            if self.state == "walk":
                self.walk_sound.stop()
            elif self.state == "meow":
                self.meow_sound.stop()
            self.state = new_state
            self.frame_data = getattr(self.data, new_state)
            self.current_frame = 0

            if new_state == "walk":
                self.direction = random.choice([-1,1])
                self.walk_sound.play()
            elif new_state == "meow":
                self.meow_sound.play()

    def transitionState(self): 
        next_states = {
            "idle": ["meow", "walk", "itch", "licking1", "sitting"], 
            "walk": ["idle", "meow", "stretching"],
            "meow": ["idle"],
            "sitting": ["lay", "licking2"],
            "lay": ["sleeping1"],
            "sleeping1": ["sleeping2"],
            "sleeping2": ["idle", "stretching"],
            "itch": ["idle"],
            "licking1": ["licking2", "idle"],
            "licking2": ["idle", "stretching"],
            "stretching": ["idle", "meow"]
        }
        options = next_states.get(self.state, ["idle"])
        self.setState(random.choice(options))

        self.state_timer = QTimer()
        self.state_timer.setSingleShot(True)
        self.state_timer.timeout.connect(self.transitionState)
        self.state_timer.start(self.duration())

    def animate(self):
        # Draw + cycle through frames
        frame = self.frame_data[self.current_frame]
        self.current_frame = (self.current_frame + 1) % len(self.frame_data)
        self.parent.label.setPixmap(frame)

        # flip sprite
        if self.direction == -1:
            transform = QTransform().scale(-1, 1)
            frame = frame.transformed(transform, mode = Qt.SmoothTransformation)
        self.parent.label.setPixmap(frame)

        # Walk movement
        if self.state == "walk":
            # adjust pos
            self.position.setX(self.position.x() + 3 * self.direction)
            # stay in bounds
            if self.position.x() < 600 or self.position.x() + self.parent.size > (self.parent.monitor.width - 200):
                self.direction *= -1
            # move
            self.parent.label.move(self.position)

        