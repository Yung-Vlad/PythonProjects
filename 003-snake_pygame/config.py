# Constants
winSizes = ["640x480", "1080x720", "FULL SCREEN"]
speed = 5
FPS = 60
SIZE = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Gaming variables
W, H = 1080, 720


class ControlOption:
    WASD = 0
    ARROWS = 1


class Difficulty:
    EASY = 0
    NORMAL = 1


difficulties = {
    0: "Easy",
    1: "Hard"
}

controls = {
    0: "WASD",
    1: "↑←↓→"
}
