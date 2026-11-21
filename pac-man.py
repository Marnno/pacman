"""Entry point: python3 pac-man.py config.json."""

import sys

import pygame

from game import Game
from maze import MazeError


def main() -> int:
    """Start the game and handle fatal errors without traceback.

    Returns:
        The exit status of the program.
    """
    try:
        Game().run()
    except MazeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except pygame.error as e:
        print(f"Error: pygame: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
