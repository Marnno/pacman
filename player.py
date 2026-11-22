from maze import DIRECTIONS, Maze


class Player:
    def __init__(self, maze: Maze) -> None:
        self.pos = [int(maze.width//2), int(maze.height // 2)]
        self.maze = maze
        self.timer = 0.0
        self.current: int | None = None
        self.wanted: int | None = None

    def player_pos(self) -> list[int]:
        return self.pos

    def can_move(self, direction: int) -> bool:
        x, y = self.pos
        return not self.maze.has_wall(x, y, direction)

    def player_input(self, direction: int) -> None:
        self.wanted = direction

    def update(self, dt: float) -> None:
        self.timer += dt
        if self.timer >= 0.3:
            self.timer %= 0.3 
            self.step()

    def step(self) -> None:
        if self.wanted is not None and self.can_move(self.wanted):
            self.current = self.wanted
        if self.current is not None and self.can_move(self.current):
            dx, dy = DIRECTIONS[self.current]
            self.pos[0] += dx
            self.pos[1] += dy
       
