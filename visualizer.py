from abc import ABC, abstractmethod

class Visualizer(ABC):
    def __init__(self, grid, paths=None, cluster_map=None):
        self._grid = grid
        self._paths = paths or []
        self._cluster_map = cluster_map or {}

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def display_metrics(self, stats):
        pass

    @abstractmethod
    def highlight_path(self, path):
        pass

    def render_clusters(self, centroids):
        """Optional: overlay cluster zones on visualization"""
        pass