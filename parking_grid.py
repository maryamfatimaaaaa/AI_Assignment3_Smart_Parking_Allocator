import random

class ParkingGrid:
    def __init__(self, rows, cols, gate, occ_percent):
        self.rows = rows
        self.cols = cols
        self.gate = gate  # (gate_row, gate_col)
        self.occupancy_rate = occ_percent
        self.grid = None
        self.display_grid = None
        self.free_slots = set()
        self.adjacency = {}
        self._build_grid()
        self._initialize_occupancy()
        self._build_display_grid()
        self._build_adjacency()

    def _build_grid(self):
        """Initialize logical grid with zeros"""
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.grid[self.gate[0]][self.gate[1]] = "S"

    def _initialize_occupancy(self):
        """Place occupied spots using weighted random sampling"""
        total_cells = self.rows * self.cols
        occupied_cells = (total_cells * self.occupancy_rate) // 100

        candidates = []
        weights = []
        for i in range(self.rows):
            for j in range(self.cols):
                if i == self.gate[0] and j == self.gate[1]:
                    continue
                dist = abs(i - self.gate[0]) + abs(j - self.gate[1])
                candidates.append((i, j))
                weights.append(1.0 / (dist + 1))

        count = 0
        available = list(range(len(candidates)))
        while count < occupied_cells and len(available) > 0:
            total_weight = sum(weights[idx] for idx in available)
            threshold = random.random() * total_weight
            running = 0.0
            chosen_pos = available[-1]
            for idx in available:
                running += weights[idx]
                if running >= threshold:
                    chosen_pos = idx
                    break
            row, col = candidates[chosen_pos]
            self.grid[row][col] = 1
            available.remove(chosen_pos)
            count += 1

        # Populate free_slots set
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == 0:
                    self.free_slots.add((i, j))

    def _build_display_grid(self):
        """Build expanded display grid with road lanes"""
        disp_rows = 2 * self.rows + 1
        disp_cols = self.cols + 2
        display = [[' ' for _ in range(disp_cols)] for _ in range(disp_rows)]

        for i in range(disp_rows):
            for j in range(disp_cols):
                if j == 0 or j == disp_cols - 1:
                    display[i][j] = ' '
                elif i == 0 or i == disp_rows - 1:
                    display[i][j] = ' '
                elif i % 2 == 0:
                    display[i][j] = ' '
                else:
                    log_row = (i - 1) // 2
                    log_col = j - 1
                    display[i][j] = self.grid[log_row][log_col]
        self.display_grid = display
        self._disp_rows = disp_rows
        self._disp_cols = disp_cols

    def _build_adjacency(self):
        """Build adjacency mapping for display grid (optimization for A*)"""
        # Simplified: adjacency is computed on the fly in A* using is_road_cell
        pass

    def is_road_cell(self, row, col):
        """Check if a display grid cell is a road"""
        if col == 0 or col == self._disp_cols - 1:
            return True
        if row == 0 or row == self._disp_rows - 1:
            return True
        if row % 2 == 0:
            return True
        return False

    def logical_to_display(self, log_row, log_col):
        """Convert logical coordinates to display coordinates"""
        return 2 * log_row + 1, log_col + 1

    def reserve_slot(self, slot):
        """Mark a logical slot as reserved (occupied for future cars)"""
        if slot in self.free_slots:
            self.free_slots.remove(slot)
            self.grid[slot[0]][slot[1]] = 1
            # Update display grid
            dr, dc = self.logical_to_display(slot[0], slot[1])
            self.display_grid[dr][dc] = 1
        else:
            self.grid[slot[0]][slot[1]] = 1

    def get_free_slots(self):
        """Return set of free slots in logical coordinates"""
        return self.free_slots

    def get_display_cell(self, row, col):
        """Get value at display grid cell"""
        return self.display_grid[row][col]
    def get_slots_in_zone(self, zone_slots):
        """Convert zone slot list (logical coordinates) to display coordinates for A*"""
        # zone_slots is already a list of (row, col) logical coordinates
        # This method exists for clarity - A* expects logical coordinates anyway
        return zone_slots