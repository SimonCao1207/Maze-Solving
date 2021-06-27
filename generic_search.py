from __future__ import annotations
from typing import TypeVar, Iterable, Sequence, Generic, List, Callable, Set, Deque, Mapping, Dict, Any, Optional
from typing_extensions import Protocol
from heapq import heappush, heappop

T = TypeVar('T')

def linear_contains(iterable: Iterable[T], key: T) -> bool:
	for item in iterable:
		if item == key:
			return True
	return False


C = TypeVar("C", bound="Comparable")

class Comparable(Protocol):
	def __eq__(self, other: Any) -> bool:
		...
	def __lt__(self: C, orther: C) -> bool:
		...
	
	def __gt__(self: C, other: C) -> bool:
		return (not self < other) and self != other

	def __le__(self: C, other: C) -> bool:
		return self < other or self == other

	def __ge__(self: C, other: C) -> bool:
		return not self < other

def binary_contains(sequence: Sequence[C], key: C) -> bool:
	low: int = 0
	high: int = len(sequence) - 1
	while low <= high:
		mid: int = (low + high) // 2
		if sequence[mid] < key:
			low = mid + 1
		elif sequence[mid] > key:
			high = mid - 1
		else:
			return True
	return False

class Stack(Generic[T]):
	def __init__(self) -> None:
		self._container: List[T] = []
	@property
	def empty(self) -> bool:
		return not self._container
	def push(self, item:T) -> None:
		self._container.append(item)
	def pop(self) -> T:
		return self._container.pop()
	def __repr__(self) -> str:
		return repr(self._container)

class Queue(Generic[T]):
	def __init__(self) -> None:
		self._container: Deque[T] = Deque()

	@property
	def empty(self) -> bool:
		return not self._container
	def push(self, item:T) -> None:
		self._container.append(item)
	def pop(self) -> T:
		return self._container.popleft()
	def __repr__(self) -> str:
		return repr(self._container)


class Node(Generic[T]):
	def __init__(self,
		state: T,
		parent: Optional[Node],
		cost: float = 0.0,
		heuritic: float = 0.0) -> None:

		self.state: T =  state
		self.parent: Optional[Node] = parent
		self.cost: float = cost
		self.heuritic:float = heuritic

	def __lt__(self, other:Node) -> bool:
		return (self.cost + self.heuritic) < (other.cost + other.heuritic)

def dfs(initial: T, goal_test: Callable[[T], bool], 
		successors: Callable[[T], List[T]]) -> Optional[Node[T]]:
		
	frontier: Stack[Node[T]] = Stack()
	frontier.push(Node(initial, None))
	explored: Set[T] = {initial}
	while not frontier.empty:
		currentNode: Node[T] = frontier.pop()
		currentState: T = currentNode.state
		if goal_test(currentState):
			return currentNode
		for child in successors(currentState):
			if child in explored:
				continue
			explored.add(child)
			frontier.push(Node(child, currentNode))
	return None

def bfs(initial: T, goal_test: Callable[[T], bool],
		successors: Callable[[T], List[T]]) -> Optional[Node[T]]:
	frontier: Queue[Node[T]] = Queue()
	frontier.push(Node(initial, None))
	explored: Set[T] = {initial}
	while not frontier.empty:
		currentNode: Node[T] = frontier.pop()
		currentState: T = currentNode.state
		if goal_test(currentState):
			return currentNode
		for child in successors(currentState):
			if child in explored:
				continue
			explored.add(child)
			frontier.push(Node(child, currentNode))
	return None

def node_to_path(node: Node[T]) -> List[T]:
	path: List[T] = [node.state]
	while node.parent is not None:
		node = node.parent
		path.append(node.state)
	path.reverse()
	return path

if __name__ == '__main__':
	print(linear_contains([1,4,14], 4))
	print(binary_contains(['a', 'd', 'e', 'f', 'g'], 'd'))