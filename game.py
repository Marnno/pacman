"""Main game class: window, game loop and events."""

import time

import pygame

from maze import Maze
from renderer import Renderer
from enum import Enum, auto
from menu import Menu
from player import Player
from player2 import Player2
from maze import EAST, NORTH, SOUTH, WEST

FPS = 60
SCREEN_RATIO = 0.95
MAX_CELL = 100
MIN_CELL = 4


class GameState(Enum):
    MAIN_MENU = auto()
    INSTRUCTIONS = auto()
    HIGH_SCORES = auto()
    PLAYING = auto()
    PAUSE = auto()
    WIN = auto()
    LOSE = auto()


class Game:
    """Own the window and run the game loop."""

    def __init__(self, width: int = 21, height: int = 21,
                 seed: int = 4) -> None:
        """Generate the first level and open the window.

        Args:
            width: Maze width in cells.
            height: Maze height in cells.
            seed: Seed of the first level.

        Raises:
            MazeError: If the maze cannot be generated.
            pygame.error: If the window cannot be opened.
        """
        self.maze: Maze = Maze(width, height, seed)
        pygame.init()
        cell = self.fit_cell(width, height)
        info = pygame.display.Info()
        self.screen: pygame.Surface = pygame.display.set_mode(
            (int(info.current_w * SCREEN_RATIO),
             int(info.current_h * SCREEN_RATIO)))
        pygame.display.set_caption("Pac-Man")
        self.renderer: Renderer = Renderer(self.screen, cell)
        self.maze_surface: pygame.Surface = (
            self.renderer.build_maze_surface(self.maze))
        self.running: bool = False
        self.state = GameState.MAIN_MENU
        self.menu = Menu(self.screen)
        self.player = Player(self.maze)
        self.player2 = Player2(self.maze)

    @staticmethod
    def fit_cell(width: int, height: int) -> int:
        """Return the biggest cell size so the maze fits on the screen.

        Must be called after pygame.init() and before set_mode(),
        otherwise pygame returns the window size instead of the screen.

        Args:
            width: Maze width in cells.
            height: Maze height in cells.

        Returns:
            The cell size in pixels, between MIN_CELL and MAX_CELL.
        """
        info = pygame.display.Info()
        screen_w = int(info.current_w * SCREEN_RATIO)
        screen_h = int(info.current_h * SCREEN_RATIO)
        if screen_w <= 0 or screen_h <= 0:
            return MAX_CELL
        cell = min(screen_w // width, screen_h // height)
        return max(MIN_CELL, min(MAX_CELL, cell))

    def handle_events(self) -> None:
        """Read keyboard and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                self.running = False
            elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_SPACE
                    and self.state == GameState.MAIN_MENU):
                self.state = GameState.PLAYING
                print(self.state)
            elif (self.state == GameState.MAIN_MENU):
                event = self.menu.event(event)
                if event == "Start Game":
                    self.state = GameState.PLAYING
                elif event == "Exit":
                    self.running = False
            elif (self.state == GameState.PLAYING and event.type == pygame.KEYDOWN):
                # Player 1: WASD
                if event.key == pygame.K_w:
                    self.player.player_input(NORTH)
                if event.key == pygame.K_d:
                    self.player.player_input(EAST)
                if event.key == pygame.K_s:
                    self.player.player_input(SOUTH)
                if event.key == pygame.K_a:
                    self.player.player_input(WEST)
                # Player 2: arrows
                if event.key == pygame.K_UP:
                    self.player2.player_input(NORTH)
                if event.key == pygame.K_RIGHT:
                    self.player2.player_input(EAST)
                if event.key == pygame.K_DOWN:
                    self.player2.player_input(SOUTH)
                if event.key == pygame.K_LEFT:
                    self.player2.player_input(WEST)

    def update(self, dt: float) -> None:
        """Update the game logic (player, ghosts, timer...).

        Args:
            dt: Time elapsed since the last frame, in seconds.
        """
        if self.state == GameState.PLAYING:
            self.player.update(dt)
            self.player2.update(dt)

    def draw(self) -> None:
        """Draw the current frame and show it."""
        if self.state == GameState.PLAYING:
            self.renderer.draw(self.maze_surface, self.player, self.player2)
        if self.state == GameState.MAIN_MENU:
            self.menu.draw()
        pygame.display.flip()

    def run(self) -> None:
        """Run the game loop until the window is closed."""
        self.running = True
        last = time.monotonic()
        try:
            while self.running:
                now = time.monotonic()
                dt = now - last
                last = now
                self.handle_events()
                self.update(dt)
                self.draw()
                elapsed = time.monotonic() - now
                time.sleep(max(0.0, 1 / FPS - elapsed))
        finally:
            pygame.quit()
