from visualizer import Visualizer

class ConsoleVisualizer(Visualizer):
    def __init__(self, grid, paths=None, cluster_map=None):
        super().__init__(grid, paths, cluster_map)

    def render(self):
        """Print ASCII grid to console"""
        disp_rows = 2 * self._grid.rows + 1
        disp_cols = self._grid.cols + 2

        # Build display grid with paths marked
        display = [row[:] for row in self._grid.display_grid]

        # Mark path roads with '*'
        for path in self._paths:
            for i in range(len(path) - 1):
                x1, y1 = path[i]
                x2, y2 = path[i+1]
                road_row = x1 + (x2 - x1)
                road_col = y1 + (y2 - y1)
                if 0 <= road_row < disp_rows and 0 <= road_col < disp_cols:
                    display[road_row][road_col] = '*'

        # Print grid
        for row in display:
            print("\t".join(str(cell) for cell in row))

    def display_metrics(self, stats):
        print(f"Allocated Parking Spot: Row = {stats.get('spot_row')}, Column = {stats.get('spot_col')}")
        print(f"Total Path Cost (moves): {stats.get('path_cost')}")
        print(f"Total Cells in Path: {stats.get('path_length')}")

    def highlight_path(self, path):
        # Path marking is handled in render
        pass