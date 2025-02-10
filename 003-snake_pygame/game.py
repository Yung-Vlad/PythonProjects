import pygame as pg
from menu import Menu
from config import *
from random import randint
from collections import deque


class Dir:
    left = right = down = up = False


class SnakeGame:
    def __init__(self):
        # Initialize pyGame
        pg.init()
        info = pg.display.Info()
        pg.display.set_caption("Snake")

        # Game settings
        self.surface = pg.display.set_mode((W, H), pg.FULLSCREEN)
        self.clock = pg.time.Clock()
        self.FONT = pg.font.SysFont("Times New Roman", 50)
        self.control = ControlOption.WASD
        self.difficulty = Difficulty.EASY
        self.virtual_surf = pg.Surface((W, H))
        self.curr_size = self.surface.get_size()
        self.FULL_SCREEN = (info.current_w, info.current_h)
        self.bg_img = pg.image.load("assets/menu.jpg")

    def run(self):
        self.starting_menu()

    # Main menu
    def starting_menu(self):
        self.create_menu({
            "Start": self.start_game,
            "Settings": self.settings,
            "Exit": self.exit_game
        })

    # Game settings menu
    def settings(self):
        self.create_menu({
            "Control": self.change_control,
            "Difficulty": self.change_difficulty,
            "Screen": self.change_screen,
            "Back": self.starting_menu
        })

    # Creating menu
    def create_menu(self, options, changed=None):
        menu = Menu(self.FONT)
        if not changed:
            for text, callback in options.items():
                menu.add_option(text, callback)
        elif changed == "SCREEN":
            for text in winSizes:
                menu.add_option(text, self.settings)
        else:
            for text in options.values():
                menu.add_option(text, self.settings)

        self.run_menu(menu, changed)

    # Drawing and selecting options
    def run_menu(self, menu, changed=None):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                elif event.type == pg.KEYDOWN:
                    if event.key in (pg.K_w, pg.K_UP):
                        menu.switch(-1)
                    elif event.key in (pg.K_s, pg.K_DOWN):
                        menu.switch(1)
                    elif event.key in (pg.K_SPACE, pg.K_RETURN):
                        if changed:
                            self.changing(changed, menu.curr_option)
                        menu.select()

            self.bg_img = pg.transform.scale(self.bg_img, self.curr_size)
            self.virtual_surf.blit(self.bg_img, (0, 0))

            if changed == "SCREEN":
                menu.draw(self.virtual_surf, 175, 100, 100)
            elif len(menu.options) == 3:
                menu.draw(self.virtual_surf, 250, 100, 100)
            elif len(menu.options) == 2:
                menu.draw(self.virtual_surf, 250, 150, 100)
            else:
                menu.draw(self.virtual_surf, 250, 50, 100)
            scaled_surf = pg.transform.scale(self.virtual_surf, self.curr_size)
            self.surface.blit(scaled_surf, (0, 0))
            pg.display.update()

    # Changing difficulty or control
    def changing(self, obj, value):
        if obj == "CTRL":
            self.control = value
        elif obj == "SCREEN":
            if value == 2:
                self.curr_size = self.FULL_SCREEN
                self.surface = pg.display.set_mode(self.curr_size, pg.FULLSCREEN)
            else:
                self.curr_size = tuple(map(int, winSizes[value].split('x')))
                self.surface = pg.display.set_mode(self.curr_size)
        else:
            self.difficulty = value

    # Main Game loop
    def start_game(self):
        # Main variables
        x, y = W // 2 - 15, H // 2 - 15
        snake_body = deque([(x, y)] * 3)
        score = appleX = appleY = 0
        is_apple_present = DirOver = False

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit_game()
                elif event.type == pg.KEYDOWN:
                    if self.control == ControlOption.WASD:
                        self.handle_movement_control1(event)
                    else:
                        self.handle_movement_control2(event)

            # Moving
            if Dir.left:
                if x < 0:
                    x = W - SIZE
                x -= speed
            elif Dir.right:
                if x > W:
                    x = 0
                x += speed
            elif Dir.up:
                if y < 0:
                    y = H - SIZE
                y -= speed
            elif Dir.down:
                if y > H:
                    y = 0
                y += speed

            # Generating apple and checking if snake ate it
            if not is_apple_present:
                appleX, appleY = self.render_apple()
                is_apple_present = True
            elif self.check_eating(x, y, appleX, appleY):
                score += 1
                pg.display.set_caption(f"Score: {score}")
                is_apple_present = False

            # Append and pop from deque(snake body)
            snake_body.appendleft((x, y))
            if len(snake_body) > score + 3:
                snake_body.pop()

            if len(snake_body) >= 10 and self.collision(snake_body):
                self.game_over(score)

            # Updates
            if not DirOver:
                self.draw_game(snake_body, appleX, appleY, score)
                self.clock.tick(FPS)

    def draw_game(self, snake_body, appleX: int, appleY: int, score: int) -> None:
        self.virtual_surf.fill(WHITE)
        self.virtual_surf.blit(self.FONT.render(f"Score: {score}", True, BLACK), (450, 0))

        # Head
        for segment in list(snake_body)[:3]:
            pg.draw.rect(self.virtual_surf, YELLOW, (segment[0], segment[1], SIZE, SIZE))

        # Body
        for segment in list(snake_body)[3:]:
            rect = pg.Rect(segment[0], segment[1], SIZE, SIZE)
            pg.draw.rect(self.virtual_surf, GREEN, rect)

        pg.draw.rect(self.virtual_surf, RED, (appleX, appleY, SIZE, SIZE))  # Apple

        scaled_surf = pg.transform.scale(self.virtual_surf, self.curr_size)
        self.surface.blit(scaled_surf, (0, 0))
        pg.display.update()

    def game_over(self, score: int) -> None:
        self.virtual_surf.fill(WHITE)
        self.virtual_surf.blit(self.FONT.render(f"Game OVER!!! Score: {score}", True, BLACK), (300, 50))
        scaled_surf = pg.transform.scale(self.virtual_surf, self.curr_size)
        self.surface.blit(scaled_surf, (0, 0))
        pg.display.update()
        pg.time.delay(2000)
        self.starting_menu()

    # Control 1: WASD
    def handle_movement_control1(self, event) -> None:
        if event.key == pg.K_a and not Dir.right:
            Dir.right = Dir.up = Dir.down = False
            Dir.left = True
        elif event.key == pg.K_d and not Dir.left:
            Dir.left = Dir.up = Dir.down = False
            Dir.right = True
        elif event.key == pg.K_w and not Dir.down:
            Dir.left = Dir.right = Dir.down = False
            Dir.up = True
        elif event.key == pg.K_s and not Dir.up:
            Dir.left = Dir.up = Dir.right = False
            Dir.down = True
        elif event.key == pg.K_ESCAPE:
            self.pause()

    # Control 2: ↑←↓→
    def handle_movement_control2(self, event) -> None:
        if event.key == pg.K_LEFT and not Dir.right:
            Dir.right = Dir.up = Dir.down = False
            Dir.left = True
        elif event.key == pg.K_RIGHT and not Dir.left:
            Dir.left = Dir.up = Dir.down = False
            Dir.right = True
        elif event.key == pg.K_UP and not Dir.down:
            Dir.left = Dir.right = Dir.down = False
            Dir.up = True
        elif event.key == pg.K_DOWN and not Dir.up:
            Dir.left = Dir.up = Dir.right = False
            Dir.down = True
        elif event.key == pg.K_ESCAPE:
            self.pause()

    # Exit Dir
    @staticmethod
    def exit_game() -> None:
        pg.quit()
        exit()

    # Render apple in random place
    @staticmethod
    def render_apple() -> (int, int):
        return randint(0, W - SIZE), randint(0, H - SIZE)

    # Check on snake ate the apple
    @staticmethod
    def check_eating(x, y, appleX, appleY) -> None:
        return (appleX - 15 <= x <= appleX + 15 and
                appleY - 15 <= y <= appleY + 15)

    # Checking whether the snake has crashed into itself
    @staticmethod
    def collision(snake) -> bool:
        head = snake[0]
        for body in list(snake)[1:]:
            if (head[0], head[1]) == (body[0], body[1]):  # If collision
                return True

        return False

    # Difficulty selection
    def change_difficulty(self) -> None:
        self.create_menu(difficulties, changed="DIFF")

    # Control selection
    def change_control(self) -> None:
        self.create_menu(controls, changed="CTRL")

    def change_screen(self) -> None:
        self.create_menu(winSizes, changed="SCREEN")

    # Pause
    def pause(self) -> None:
        paused = True
        while paused:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                elif event.type == pg.KEYDOWN:
                    if event.key in (pg.K_ESCAPE, pg.K_RETURN):
                        paused = False

            self.virtual_surf.blit(self.FONT.render("PAUSE", True, BLACK), (250, 200))
            scaled_surf = pg.transform.scale(self.virtual_surf, self.curr_size)
            self.surface.blit(scaled_surf, (0, 0))
            pg.display.update()
