import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from visualizer import Visualizer

class StreamlitVisualizer(Visualizer):
    def __init__(self, grid, paths=None, allocated_spots=None):
        super().__init__(grid, paths)
        self.allocated_spots = allocated_spots or {}

    def render(self):
        """Generate and display matplotlib figure"""
        fig, ax = plt.subplots(figsize=(16, 10), facecolor='#0f172a')
        ax.set_facecolor('#0f172a')

        display = self._grid.display_grid
        disp_rows = 2 * self._grid.rows + 1
        disp_cols = self._grid.cols + 2

        colors = {
            0: '#22c55e', 1: '#ef4444', 'S': '#3b82f6',
            'road': '#1e293b', 'path': '#fbbf24',
            'P1': '#ef4444', 'P2': '#3b82f6', 'P3': '#22c55e',
            'P4': '#f97316', 'P5': '#a855f7'
        }

        cell_size = 0.9
        spacing = 0.1

        for i in range(disp_rows):
            for j in range(disp_cols):
                cell = display[i][j]
                x = j * (cell_size + spacing)
                y = (disp_rows - 1 - i) * (cell_size + spacing)

                is_road = self._grid.is_road_cell(i, j)

                if is_road:
                    is_path = any((i, j) in p for p in self._paths)
                    facecolor = colors['path'] if is_path else colors['road']
                    edgecolor = '#f59e0b' if is_path else '#475569'
                    linewidth = 2.5 if is_path else 1
                    rect = plt.Rectangle((x, y), cell_size, cell_size, linewidth=linewidth,
                                         edgecolor=edgecolor, facecolor=facecolor, alpha=0.9, zorder=1)
                    ax.add_patch(rect)
                else:
                    log_row = (i - 1) // 2
                    log_col = j - 1
                    if self.allocated_spots and (log_row, log_col) in self.allocated_spots:
                        car_label = self.allocated_spots[(log_row, log_col)]
                        facecolor = colors.get(car_label, colors['P1'])
                        edgecolor = '#fbbf24'
                        linewidth = 3
                    elif cell == 0:
                        facecolor = colors[0]
                        edgecolor = '#166534'
                        linewidth = 1.5
                    elif cell == 1:
                        facecolor = colors[1]
                        edgecolor = '#991b1b'
                        linewidth = 1.5
                    elif cell == 'S':
                        facecolor = colors['S']
                        edgecolor = '#1e40af'
                        linewidth = 3
                    else:
                        facecolor = '#1e293b'
                        edgecolor = '#475569'
                        linewidth = 1

                    rect = plt.Rectangle((x, y), cell_size, cell_size, linewidth=linewidth,
                                         edgecolor=edgecolor, facecolor=facecolor, alpha=0.95, zorder=2)
                    ax.add_patch(rect)

                    if cell == 'S':
                        ax.text(x + cell_size/2, y + cell_size/2, 'GATE',
                                ha='center', va='center', fontsize=9, fontweight='bold', color='white')
                    elif self.allocated_spots and (log_row, log_col) in self.allocated_spots:
                        car_num = self.allocated_spots[(log_row, log_col)][1:] if self.allocated_spots[(log_row, log_col)].startswith('P') else self.allocated_spots[(log_row, log_col)]
                        ax.text(x + cell_size/2, y + cell_size/2, car_num,
                                ha='center', va='center', fontsize=14, fontweight='bold', color='white',
                                bbox=dict(boxstyle="circle,pad=0.3", facecolor=edgecolor, edgecolor='white', linewidth=2))
                        ax.text(x + cell_size/2, y + cell_size/2 - 0.25, 'CAR',
                                ha='center', va='center', fontsize=7, fontweight='bold', color='white', alpha=0.9)

        # Draw path lines
        if self._paths:
            path_styles = ['#ef4444', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6']
            for p_idx, path in enumerate(self._paths):
                if len(path) > 1:
                    for k in range(len(path)-1):
                        x1 = path[k][1] * (cell_size + spacing) + cell_size/2
                        y1 = (disp_rows - 1 - path[k][0]) * (cell_size + spacing) + cell_size/2
                        x2 = path[k+1][1] * (cell_size + spacing) + cell_size/2
                        y2 = (disp_rows - 1 - path[k+1][0]) * (cell_size + spacing) + cell_size/2
                        ax.plot([x1, x2], [y1, y2], color=path_styles[p_idx % len(path_styles)],
                                linewidth=4, alpha=0.9, zorder=4, solid_capstyle='round')

        # Labels
        for i in range(self._grid.rows):
            y_pos = (disp_rows - 1 - (2*i + 1)) * (cell_size + spacing) + cell_size/2
            ax.text(-0.5, y_pos, str(i), ha='right', va='center', fontsize=10, fontweight='bold', color='white')
        for j in range(self._grid.cols):
            x_pos = (j + 1) * (cell_size + spacing) + cell_size/2
            ax.text(x_pos, -0.5, str(j), ha='center', va='top', fontsize=10, fontweight='bold', color='white')

        ax.set_xlim(-1, disp_cols * (cell_size + spacing))
        ax.set_ylim(-1, disp_rows * (cell_size + spacing) + 1)
        ax.set_aspect('equal')
        ax.axis('off')

        if self._paths:
            ax.text(disp_cols * (cell_size + spacing) / 2, disp_rows * (cell_size + spacing) + 0.8,
                    f'{len(self._paths)} VEHICLE(S) PARKED', ha='center', va='center',
                    fontsize=16, fontweight='bold', color='white',
                    bbox=dict(boxstyle="round,pad=0.6", facecolor='#0f172a', edgecolor='#fbbf24', linewidth=3))

        return fig

    def display_metrics(self, stats):
        """Display metrics in Streamlit (handled in controller)"""
        pass

    def highlight_path(self, path):
        pass