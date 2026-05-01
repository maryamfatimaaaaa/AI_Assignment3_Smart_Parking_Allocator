from parking_grid import ParkingGrid
from a_star_search import AStarSearch
from k_means_clusterer import KMeansClusterer
from console_visualizer import ConsoleVisualizer
from streamlit_visualizer import StreamlitVisualizer
from input_handler import InputHandler
class Controller:
    _instance = None

    @staticmethod
    def get_instance():
        if Controller._instance is None:
            Controller._instance = Controller()
        return Controller._instance

    def __init__(self):
        self.parking_grid = None
        self.search_engine = None
        self.clusterer = None
        self.visualizer = None
        self.n_cars = 0
        self.all_paths = []
        self.allocated_spots = {}
        self.reserved_slots = set()
        self.nodes_list = []
        self.num_cars_parked = 0

    def run(self, params, mode='gui', num_cars=3):
        """Main execution entry point with K-Means zone restriction"""
        rows = params['rows']
        cols = params['cols']
        gate = params['gate']
        occ = params['occupancy']

        # Build grid
        self.parking_grid = ParkingGrid(rows, cols, gate, occ)

        # Run K-Means clustering on free slots
        free = self.parking_grid.get_free_slots()
        self.clusterer = None
        self.cluster_assignments = None
        
        if free and len(free) >= 4:  # Need at least 4 slots for meaningful clusters
            self.clusterer = KMeansClusterer(free, k=min(3, len(free)//2))
            clusters = self.clusterer.cluster_slots()
            if clusters:
                self.cluster_assignments = clusters
                print(f"[K-Means] {len(clusters)} zones created from {len(free)} free slots")
        else:
            print("[K-Means] Not enough free slots for clustering - using global search")

        # Search engine
        self.search_engine = AStarSearch(self.parking_grid)

        # Allocate cars sequentially
        self.reserved_slots = set()
        self.all_paths = []
        self.allocated_spots = {}
        self.nodes_list = []
        self.num_cars_parked = 0

        for car_idx in range(num_cars):
            # Determine zone to search
            target_zone = None
            zone_slots = []
            
            if self.clusterer and self.cluster_assignments:
                # Find zone with centroid closest to gate
                min_dist = float('inf')
                for zone_id, centroid in enumerate(self.clusterer.centroids):
                    dist = abs(gate[0] - centroid[0]) + abs(gate[1] - centroid[1])
                    if dist < min_dist:
                        min_dist = dist
                        target_zone = zone_id
                
                if target_zone is not None:
                    # Get slots in this zone
                    zone_slots = self.cluster_assignments.get(target_zone, [])
                    # Filter out already reserved slots
                    zone_slots = [s for s in zone_slots if s not in self.reserved_slots]
                    self.search_engine._zone_slots = zone_slots
                    print(f"[Car {car_idx+1}] Searching Zone {target_zone} with {len(zone_slots)} slots")
                else:
                    self.search_engine._zone_slots = []
            else:
                self.search_engine._zone_slots = []

            # Run A* search
            goal = self.search_engine.search(gate, self.reserved_slots)
            
            if goal is None:
                # If zone-specific search failed, try global search
                if self.search_engine._zone_slots:
                    print(f"[Car {car_idx+1}] Zone empty, falling back to global search")
                    self.search_engine._zone_slots = []
                    goal = self.search_engine.search(gate, self.reserved_slots)
            
            if goal is None:
                break

            # Reconstruct path and reserve slot
            path = self.search_engine.reconstruct_path(goal)
            self.all_paths.append(path)
            log_r = (goal.row - 1) // 2
            log_c = goal.col - 1
            self.allocated_spots[(log_r, log_c)] = f"P{car_idx+1}"
            self.reserved_slots.add((log_r, log_c))
            self.num_cars_parked += 1

            # Update clusterer by removing the allocated slot from its zone
            if self.clusterer and target_zone is not None:
                self.clusterer.update_centroids((log_r, log_c))
                # Refresh zone assignments if needed
                if self.cluster_assignments and (log_r, log_c) in self.cluster_assignments.get(target_zone, []):
                    self.cluster_assignments[target_zone].remove((log_r, log_c))

        # Set up visualizer
        if mode == 'gui':
            self.visualizer = StreamlitVisualizer(self.parking_grid, self.all_paths, self.allocated_spots)
        else:
            self.visualizer = ConsoleVisualizer(self.parking_grid, self.all_paths)

        return self.all_paths, self.allocated_spots, self.collect_metrics()

    def collect_metrics(self):
        """Return statistics about the allocation run"""
        total_steps = sum(len(p) - 1 for p in self.all_paths) if self.all_paths else 0
        avg_nodes = sum(self.nodes_list) // len(self.nodes_list) if self.nodes_list else 0
        free_spots = len(self.parking_grid.get_free_slots()) if self.parking_grid else 0
        remaining = free_spots - self.num_cars_parked
        cluster_status = "Enabled" if self.clusterer else "Disabled (insufficient slots)"
        return {
            'parked': self.num_cars_parked,
            'avg_nodes': avg_nodes,
            'total_steps': total_steps,
            'free_left': remaining,
            'clustering': cluster_status
        }
    def allocate_cars(self):
        """Standalone car allocation (used by CLI)"""
        # Similar to run but returns only path info
        pass

    def validate_input(self, params):
        return InputHandler.validate(params)