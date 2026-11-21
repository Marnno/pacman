"""Main menu of the game."""

import pygame

from renderer import BACKGROUND
FONT_SIZE = 48
TEXT_COLOR = (255, 255, 0)
BUTTON_GAP = 30
TITLE_GAP = 50


class Menu:
    """Main menu: clickable image buttons drawn on the game window."""

    def __init__(self, window: pygame.Surface) -> None:
        """Load the buttons and centre them in the window.

        Args:
            window: The game window, opened by Game.
        """
        self.screen: pygame.Surface = window
        self.buttons: list[str] = [
            "Start Game",
            "Highscores",
            "Instructions",
            "Exit",
        ]
        self.selected: int = 0
        self.font: pygame.font.Font = pygame.font.Font(None, FONT_SIZE)
        self.images: list[pygame.Surface] = [
            pygame.image.load("./assets/menu/btn_start.png"),
            pygame.image.load("./assets/menu/btn_highscores.png"),
            pygame.image.load("./assets/menu/btn_instructions.png"),
            pygame.image.load("./assets/menu/btn_exit.png"),
        ]
        self.images_hoover: list[pygame.Surface] = [
            pygame.image.load("./assets/menu/btn_start_hover.png"),
            pygame.image.load("./assets/menu/btn_highscores_hover.png"),
            pygame.image.load("./assets/menu/btn_instructions_hover.png"),
            pygame.image.load("./assets/menu/btn_exit_hover.png"),
        ]
        self.title: pygame.Surface = pygame.image.load(
            "./assets/menu/title.png")
        self.hovered: int | None = None
        self.positions: list[tuple[int, int]] = []
        total_h = (self.title.get_height() + TITLE_GAP
                   + sum(img.get_height() for img in self.images)
                   + BUTTON_GAP * (len(self.images) - 1))
        y = (self.screen.get_height() - total_h) // 2
        title_x = (self.screen.get_width() - self.title.get_width()) // 2
        self.title_pos: tuple[int, int] = (title_x, y)
        y += self.title.get_height() + TITLE_GAP
        for img in self.images:
            x = (self.screen.get_width() - img.get_width()) // 2
            self.positions.append((x, y))
            y += img.get_height() + BUTTON_GAP

    def button_at(self, mx: int, my: int) -> int | None:
        """Return the index of the button under (mx, my), or None.

        Args:
            mx: Mouse x position in the window.
            my: Mouse y position in the window.
        """
        for i in range(len(self.images)):
            x, y = self.positions[i]
            w = self.images[i].get_width()
            h = self.images[i].get_height()
            if x <= mx < x + w and y <= my < y + h:
                return i
        return None

    def event(self, event: pygame.event.Event) -> str | None:
        """Update the hovered button and return the clicked one.

        Args:
            event: A pygame event forwarded by Game.

        Returns:
            The label of the clicked button, or None.
        """
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.button_at(*event.pos)
            return None
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            i = self.button_at(*event.pos)
            if i is not None:
                return self.buttons[i]
        return None

    def draw(self) -> None:
        """Draw the background and every button, hovered one highlighted."""
        self.screen.fill(BACKGROUND)
        self.screen.blit(self.title, self.title_pos)
        for i in range(len(self.images)):
            if i == self.hovered:
                self.screen.blit(self.images_hoover[i], self.positions[i])
            else:
                self.screen.blit(self.images[i], self.positions[i])
