from node import Node
from min_heap import MinHeap
from search_algorithm import SearchAlgorithm

class AStarSearch(SearchAlgorithm):
    def __init__(self, parking_grid):
        super().__init__(parking_grid)
        self._disp_rows = 2 * parking_grid.rows + 1
        self._disp_cols = parking_grid.cols + 2

    def heuristic(self, disp_row, disp_col):
        """Manhattan distance to nearest free slot in current zone (if set)"""
        min_dist = 99999
        free_found = False
        
        # CRITICAL: If zone_slots is set, ONLY search within that zone
        if self._zone_slots:
            target_slots = self._zone_slots
        else:
            target_slots = self._parking_grid.get_free_slots()
        
        for log_r, log_c in target_slots:
            dr, dc = self._parking_grid.logical_to_display(log_r, log_c)
            dist = abs(disp_row - dr) + abs(disp_col - dc)
            if dist < min_dist:
                min_dist = dist
                free_found = True
        
        # If zone has no free slots, fall back to global search
        if not free_found and self._zone_slots:
            # Zone is full - fall back to all free slots
            for log_r, log_c in self._parking_grid.get_free_slots():
                dr, dc = self._parking_grid.logical_to_display(log_r, log_c)
                dist = abs(disp_row - dr) + abs(disp_col - dc)
                if dist < min_dist:
                    min_dist = dist
                    free_found = True
        
        return min_dist if free_found else 99999
    def search(self, start, reserved=None):
        """Run A* from start cell (logical coordinates) to nearest free slot"""
        self._reserved_slots = reserved or set()
        start_disp_r, start_disp_c = self._parking_grid.logical_to_display(start[0], start[1])

        start_h = self.heuristic(start_disp_r, start_disp_c)
        start_node = Node(start_disp_r, start_disp_c, 0, start_h, None)

        open_list = MinHeap()
        closed_list = set()
        open_list.push(start_node)

        goal_node = None
        nodes_explored = 0

        while not open_list.is_empty():
            current = open_list.pop()
            nodes_explored += 1

            # Check if current is a free parking slot
            if (current.row % 2 == 1 and
                0 < current.col < self._disp_cols - 1 and
                self._parking_grid.get_display_cell(current.row, current.col) == 0):
                # Convert to logical to check reservation
                log_r = (current.row - 1) // 2
                log_c = current.col - 1
                if (log_r, log_c) not in self._reserved_slots:
                    goal_node = current
                    break

            closed_list.add((current.row, current.col))

            # Expand neighbors
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = current.row + dr, current.col + dc

                # Bounds check
                if nr < 0 or nr >= self._disp_rows or nc < 0 or nc >= self._disp_cols:
                    continue

                # Check if valid move (road or legal parking entry)
                is_road = self._parking_grid.is_road_cell(nr, nc)
                if not is_road:
                    # Parking cell — only allowed from road cell
                    if not self._parking_grid.is_road_cell(current.row, current.col):
                        continue
                    cell_val = self._parking_grid.get_display_cell(nr, nc)
                    if cell_val == 1:  # Occupied
                        continue
                    if cell_val == 'S':  # Gate
                        continue
                    log_r = (nr - 1) // 2
                    log_c = nc - 1
                    if (log_r, log_c) in self._reserved_slots:
                        continue

                if (nr, nc) in closed_list:
                    continue
                if any(n.row == nr and n.col == nc for n in open_list.heap):
                    continue

                new_g = current.g + 1
                new_h = self.heuristic(nr, nc)
                new_node = Node(nr, nc, new_g, new_h, current)
                open_list.push(new_node)

        if goal_node:
            print(f"\nGoal Found at: ({goal_node.row}, {goal_node.col})")
            print(f"Total nodes explored: {nodes_explored}")
            return goal_node
        return None

    def reconstruct_path(self, goal):
        path = []
        cur = goal
        while cur:
            path.append((cur.row, cur.col))
            cur = cur.parent
        return list(reversed(path))