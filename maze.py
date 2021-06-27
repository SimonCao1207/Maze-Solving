from enum import Enum
from typing import List, NamedTuple, Callable, Optional
import random
from math import sqrt
from generic_search import dfs, bfs, node_to_path, Node
from gui import *

class Cell(str, Enum):
	EMPTY = " "
	BlOCKED = "X"
	START = "S"
	GOAL = "G"
	PATH = "*"


class MazeLocation(NamedTuple):
	row: int
	column: int


class Maze:
	def __init__(self, rows: int = 10, columns: int = 10,
		sparseness: float = 0.2,
		start: MazeLocation = MazeLocation(0, 0),
		goal: MazeLocation = MazeLocation(9, 9),
		) -> None:
		self._rows: int = rows
		self._columns: int = columns
		self.start = start
		self.goal = goal
		self._grid : List[List[Cell]] = [[Cell.EMPTY for c in range(columns)]
		for r in range(rows)]
		
		self._randomly_fill(rows, columns, sparseness)

		self._grid[start.row][start.column] = Cell.START
		self._grid[goal.row][goal.column] = Cell.GOAL

	def _randomly_fill(self, rows: int, columns: int, sparseness: float):
		for row in range(rows):
			for column in range(columns):
				if random.uniform(0, 1.0) < sparseness:
					self._grid[row][column] = Cell.BlOCKED

	# return a nicely formatted version of the maze for printing
	def __str__(self) -> str:
		output: str = ""
		for row in self._grid:
			output += " ".join([c.value for c in row]) + "\n"
		return output

	def goal_test(self, loc: MazeLocation) -> bool:
		return loc == self.goal

	def succesors(self, loc: MazeLocation) -> List[MazeLocation]:
		locations: List[MazeLocation] = []
		
		#GO DOWN
		if loc.row + 1 < self._rows and self._grid[loc.row + 1][loc.column] != Cell.BlOCKED:
			locations.append(MazeLocation(loc.row + 1, loc.column))

		#GO UP
		if loc.row - 1 >=  0 and self._grid[loc.row - 1][loc.column] != Cell.BlOCKED:
			locations.append(MazeLocation(loc.row - 1, loc.column))

		#GO RIGHT
		if loc.column + 1 < self._columns and self._grid[loc.row][loc.column + 1] != Cell.BlOCKED:
			locations.append(MazeLocation(loc.row, loc.column + 1))

		#GO LEFT
		if loc.column - 1 >= 0 and self._grid[loc.row][loc.column - 1] != Cell.BlOCKED:
			locations.append(MazeLocation(loc.row, loc.column - 1))
		return locations

	def mark(self, path: List[MazeLocation]):
		for loc in path:
			self._grid[loc.row][loc.column] = Cell.PATH
		self._grid[self.start.row][self.start.column] = Cell.START
		self._grid[self.goal.row][self.goal.column] = Cell.GOAL

	def clear(self, path: List[MazeLocation]):
		for loc in path:
			self._grid[loc.row][loc.column] = Cell.EMPTY

	def makeCellMap(self):
		cellMAP = [[ 0 for c in range(self._columns)] for r in range(self._rows)]
		for c in range(self._columns):
			for r in range(self._rows):
				if self._grid[r][c] == Cell.BlOCKED:
					cellMAP[r][c] = 1
				elif self._grid[r][c] == Cell.PATH:
					cellMAP[r][c] = -1
				elif self._grid[r][c] == Cell.START or self._grid[r][c] == Cell.GOAL: 
					cellMAP[r][c] = 2
		return cellMAP

	def createWindow(self, name:str="Original Maze"):
		cellMAP = np.array(self.makeCellMap())
		finalGUI(cellMAP, name)

if __name__ == '__main__':
	ROWS = 10
	COLUMNS = 10
	START = MazeLocation(0, 0)
	GOAL = MazeLocation(9, 9)
	SPARSENESS = 0.2

	maze : Maze = Maze(rows=ROWS, columns=COLUMNS, start=START, goal=GOAL, sparseness=SPARSENESS)
	print(maze)
	maze.createWindow()
	print("_____________________________________")
	
	print("DFS Solution to the maze: \n")
	dfs_sol: Optional[Node[MazeLocation]] = dfs(maze.start, maze.goal_test, maze.succesors)
	if dfs_sol is None:
		print("No solution found using dfs")
	else:
		path: List[MazeLocation] = node_to_path(dfs_sol)
		maze.mark(path)
		print(maze)
		maze.createWindow("DFS Solution")
		maze.clear(path)

	print("_____________________________________")
	print("BFS Solution to the maze: \n")
	bfs_sol: Optional[Node[MazeLocation]] = bfs(maze.start, maze.goal_test, maze.succesors)
	if bfs_sol is None:
		print("No solution found using bfs")
	else:
		path: List[MazeLocation] = node_to_path(bfs_sol)
		maze.mark(path)
		print(maze)
		maze.createWindow("BFS Solution")
		maze.clear(path)




