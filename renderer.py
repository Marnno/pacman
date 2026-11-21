"""Drawing of the game with pygame.

Only pygame functions that have an MLX equivalent are used:
Surface (mlx_new_image), set_at (pixel write), fill (mlx_clear_window)
and blit (mlx_put_image_to_window).
"""
import pygame
import colorsys


from maze import Maze, NORTH, EAST, SOUTH, WEST
from player import Player
Color = tuple[int, int, int]

BACKGROUND: Color = (0, 20, 0)
WALL: Color = (0, 0, 255)
BLOCKED: Color = (255, 255, 0)
WALL_INNER: Color = (0, 0, 0)
WALL_RATIO = 8


class Renderer:
    """Draw the game on a pygame surface. Contains no game loop."""

    def __init__(self, screen: pygame.Surface, cell: int) -> None:
        """Store the target surface and the cell size.

        Args:
            screen: Surface to draw on (the window).
            cell: Size of one maze cell in pixels.
        """
        self.screen: pygame.Surface = screen
        self.cell: int = cell
        self.wall: int = max(1, cell // WALL_RATIO)
        self.pac_man: list[pygame.Surface] = [
            pygame.image.load("./assets/player/player_0.png"),
            pygame.image.load("./assets/player/player_1.png"),
            pygame.image.load("./assets/player/player_2.png"),
            pygame.image.load("./assets/player/player_3.png")]

    @staticmethod
    def draw_rect(surface: pygame.Surface, x: int, y: int,
                  w: int, h: int, color: Color) -> None:
        """Fill a rectangle pixel by pixel.

        Args:
            surface: Surface to draw on.
            x: Left position in pixels.
            y: Top position in pixels.
            w: Width in pixels.
            h: Height in pixels.
            color: RGB color.
        """
        for py in range(y, y + h):
            for px in range(x, x + w):
                surface.set_at((px, py), color)

    @staticmethod
    def rainbow(x, y):
        rainbow_period = 4000
        color = x + y
        hsv = (color / rainbow_period) % 1
        r, g, b = colorsys.hsv_to_rgb(hsv, 0.6, 1.0)
        return (int(r * 255), int(g * 255), int(b * 255))

    def build_maze_surface(self, maze: Maze) -> pygame.Surface:
        """Draw the maze once on its own surface.

        The maze does not change during a level, so it is drawn once
        and then blitted every frame.

        Args:
            maze: The maze to draw.

        Returns:
            A surface containing the drawn maze.
        """
        c = self.cell
        surface = pygame.Surface((maze.width * c, maze.height * c))
        surface.fill(BACKGROUND)
        for cy in range(maze.height):
            for cx in range(maze.width):
                x, y = cx * c, cy * c
                if maze.is_blocked(cx, cy):
                    self.draw_rect(surface, x, y, c, c, BLOCKED)
                if maze.has_wall(cx, cy, NORTH):
                    self.draw_rect(surface, x, y, c, self.wall,
                                   self.rainbow(x, y))
                if maze.has_wall(cx, cy, WEST):
                    self.draw_rect(surface, x, y, self.wall,
                                   c, self.rainbow(x, y))
                if maze.has_wall(cx, cy, SOUTH):
                    self.draw_rect(surface, x, y + c - self.wall,
                                   c, self.wall, self.rainbow(x, y))
                if maze.has_wall(cx, cy, EAST):
                    self.draw_rect(surface, x + c - self.wall, y,
                                   self.wall, c, self.rainbow(x, y))
        self.draw_wall_corners(surface, maze)
        self.draw_wall_inner(surface, maze)
        return surface

    @staticmethod
    def _h_wall(maze: Maze, cx: int, gy: int) -> bool:
        """Return True if a wall lies on grid line y=gy above cell cx.

        Args:
            maze: The maze.
            cx: Column of the cell.
            gy: Horizontal grid line, from 0 to maze.height.
        """
        if not 0 <= cx < maze.width:
            return False
        return ((gy < maze.height and maze.has_wall(cx, gy, NORTH))
                or (gy > 0 and maze.has_wall(cx, gy - 1, SOUTH)))

    @staticmethod
    def _v_wall(maze: Maze, gx: int, cy: int) -> bool:
        """Return True if a wall lies on grid line x=gx left of cell cy.

        Args:
            maze: The maze.
            gx: Vertical grid line, from 0 to maze.width.
            cy: Row of the cell.
        """
        if not 0 <= cy < maze.height:
            return False
        return ((gx < maze.width and maze.has_wall(gx, cy, WEST))
                or (gx > 0 and maze.has_wall(gx - 1, cy, EAST)))

    def _walls_at(self, maze: Maze, gx: int, gy: int) -> int:
        """Count the walls that touch the grid point (gx, gy).

        A grid point is a corner shared by up to 4 cells.

        Args:
            maze: The maze.
            gx: Vertical grid line, from 0 to maze.width.
            gy: Horizontal grid line, from 0 to maze.height.
        """
        return (self._h_wall(maze, gx, gy) + self._h_wall(maze, gx - 1, gy)
                + self._v_wall(maze, gx, gy) + self._v_wall(maze, gx, gy - 1))

    def draw_wall_corners(self, surface: pygame.Surface, maze: Maze) -> None:
        """Fill the blue square where 2 walls or more meet.

        Each cell only draws the half of a wall that is inside it. In an
        L-shaped corner, the cell on the outer side of the L has no wall,
        so its little corner square stays empty: this method fills it.

        Args:
            surface: Surface where the blue walls are already drawn.
            maze: The maze.
        """
        c, w = self.cell, self.wall
        for gy in range(maze.height + 1):
            for gx in range(maze.width + 1):
                if self._walls_at(maze, gx, gy) >= 2:
                    self.draw_rect(surface, gx * c - w, gy * c - w,
                                   2 * w, 2 * w, self.rainbow(gx * c, gy * c))

    def draw_wall_inner(self, surface: pygame.Surface, maze: Maze) -> None:
        """Draw a black line in the middle of the blue walls.

        Redraws every wall on top of the blue one, thinner and
        shortened by k pixels at each end. Then fills the grid points
        where 2 walls or more meet, so the black line stays continuous
        in corners and straight lines, but stays closed by blue at the
        end of a wall.

        Args:
            surface: Surface where the blue walls are already drawn.
            maze: The maze.
        """
        if self.wall < 2:
            return
        c = self.cell
        k = self.wall // 2
        for cy in range(maze.height):
            for cx in range(maze.width):
                x, y = cx * c, cy * c
                if maze.has_wall(cx, cy, NORTH):
                    self.draw_rect(surface, x + k, y, c - 2 * k, k,
                                   WALL_INNER)
                if maze.has_wall(cx, cy, SOUTH):
                    self.draw_rect(surface, x + k, y + c - k, c - 2 * k, k,
                                   WALL_INNER)
                if maze.has_wall(cx, cy, WEST):
                    self.draw_rect(surface, x, y + k, k, c - 2 * k,
                                   WALL_INNER)
                if maze.has_wall(cx, cy, EAST):
                    self.draw_rect(surface, x + c - k, y + k, k, c - 2 * k,
                                   WALL_INNER)
        for gy in range(maze.height + 1):
            for gx in range(maze.width + 1):
                if self._walls_at(maze, gx, gy) >= 2:
                    self.draw_rect(surface, gx * c - k, gy * c - k,
                                   2 * k, 2 * k, WALL_INNER)

    def draw(self, maze_surface: pygame.Surface, player: Player) -> None:
        """Draw one frame.

        Args:
            maze_surface: Surface returned by build_maze_surface.
            player: The player to draw on top of the maze.
        """
        self.screen.fill(BACKGROUND)
        x = (self.screen.get_width() - maze_surface.get_width()) // 2
        y = (self.screen.get_height() - maze_surface.get_height()) // 2
        self.screen.blit(maze_surface, (x, y))
        self.screen.blit(self.pac_man[0], (player.player_pos()[
                         0] * self.cell + x, player.player_pos()[1] * self.cell + y))
