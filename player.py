from maze import Maze


class Player:
    def __init__(self, maze: Maze):
        self.pos = [int(maze.width//2), int(maze.height // 2)]
        self.maze = maze

    def player_pos(self):
        return (self.pos)

    def player_input(self, pos: tuple[int, int]):
        print(self.pos)
        self.pos[0] += pos[0]
        self.pos[1] += pos[1]
        print(self.pos)
