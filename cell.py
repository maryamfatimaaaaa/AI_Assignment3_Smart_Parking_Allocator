class Cell:
    def __init__(self, row, col, cell_type):
        self.row = row
        self.col = col
        self.cell_type = cell_type
        self.is_occupied = (cell_type == 'occupied')
        self.value = 0 if cell_type == 'free' else (1 if cell_type == 'occupied' else None)

    def set_occupied(self, flag):
        self.is_occupied = flag
        self.value = 1 if flag else 0

    def is_road(self):
        return self.cell_type == 'road'

    def __repr__(self):
        return f"Cell({self.row},{self.col},{self.cell_type})"