from abc import ABC, abstractmethod

class SearchAlgorithm(ABC):
    def __init__(self, parking_grid):
        self._parking_grid = parking_grid
        self._reserved_slots = set()
        self._zone_slots = []  # Restrict search to specific zone if set

    @abstractmethod
    def search(self, start, reserved=None):
        pass

    @abstractmethod
    def heuristic(self, row, col):
        pass

    @abstractmethod
    def reconstruct_path(self, goal):
        pass