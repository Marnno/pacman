"""Wrapper around the external mazegenerator package."""

from mazegenerator import MazeGenerator

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8
BLOCKED = 15

DIRECTIONS: dict[str, tuple[int, int]] = {
    "NORTH": (0, -1),
    "EAST": (1, 0),
    "SOUTH": (0, 1),
    "WEST": (-1, 0),
}


class MazeError(Exception):
    """Raised when the maze cannot be generated."""


class Maze:
    """A Pac-Man level maze built with the external MazeGenerator.

    Each cell is an int whose 4 low bits are its walls:
    N=1, E=2, S=4, W=8. A cell equal to 15 is closed (part of the '42').

    Attributes:
        width: Number of columns.
        height: Number of rows.
        grid: 2D list of cells, accessed as grid[y][x].
    """

    def __init__(self, width: int, height: int, seed: int = 0) -> None:
        """Generate a new maze.

        Args:
            width: Number of columns.
            height: Number of rows.
            seed: Seed for reproducible mazes, 0 for random.

        Raises:
            MazeError: If the generator fails or returns an invalid maze.
        """
        self.width: int = width
        self.height: int = height
        self.grid: list[list[int]] = []
        try:
            self._generator = MazeGenerator(size=(width, height),
                                            perfect=False, seed=seed)
        except Exception as e:
            raise MazeError(f"maze generation failed: {e}") from e
        self._load()

    def regenerate(self, seed: int = 0) -> None:
        """Generate a new maze with the same size.

        Args:
            seed: Seed for reproducible mazes, 0 for random.

        Raises:
            MazeError: If the generator fails or returns an invalid maze.
        """
        try:
            self._generator.generate(seed)
        except Exception as e:
            raise MazeError(f"maze generation failed: {e}") from e
        self._load()

    def _load(self) -> None:
        """Copy and validate the grid produced by the generator."""
        grid = self._generator.maze
        if (len(grid) != self.height
                or any(len(row) != self.width for row in grid)):
            raise MazeError("generator returned a maze of the wrong size")
        self.grid = [list(row) for row in grid]

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if (x, y) is inside the maze."""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_blocked(self, x: int, y: int) -> bool:
        """Return True if the cell is closed on all sides (the '42')."""
        return self.grid[y][x] == BLOCKED

    def has_wall(self, x: int, y: int, direction: int) -> bool:
        """Return True if the cell has a wall on the given side.

        Args:
            x: Column of the cell.
            y: Row of the cell.
            direction: One of NORTH, EAST, SOUTH, WEST.
        """
        return bool(self.grid[y][x] & direction)
