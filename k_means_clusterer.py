import random

class KMeansClusterer:
    def __init__(self, free_slots, k=3):
        self.free_slots = set(free_slots)
        self.k = min(k, len(free_slots)) if free_slots else 1
        self.centroids = []
        self.cluster_assignments = {}  # slot -> zone_id

    def manhattan(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def cluster_slots(self):
        """Run K-Means clustering on free slots"""
        if not self.free_slots:
            return {}

        # Initialize centroids randomly
        slots_list = list(self.free_slots)
        self.centroids = [list(slots_list[i]) for i in random.sample(range(len(slots_list)), min(self.k, len(slots_list)))]

        for _ in range(100):  # Max iterations
            # Assign slots to nearest centroid
            new_assignments = {}
            for slot in self.free_slots:
                min_dist = float('inf')
                best_zone = 0
                for z, centroid in enumerate(self.centroids):
                    dist = self.manhattan(slot, tuple(centroid))
                    if dist < min_dist:
                        min_dist = dist
                        best_zone = z
                new_assignments[slot] = best_zone

            # Recompute centroids
            new_centroids = []
            for z in range(len(self.centroids)):
                zone_slots = [s for s, zone in new_assignments.items() if zone == z]
                if zone_slots:
                    avg_r = sum(s[0] for s in zone_slots) / len(zone_slots)
                    avg_c = sum(s[1] for s in zone_slots) / len(zone_slots)
                    new_centroids.append([avg_r, avg_c])
                else:
                    new_centroids.append(self.centroids[z])

            # Check convergence
            if all(abs( self.centroids[z][0] - new_centroids[z][0]) < 0.001 and
                   abs( self.centroids[z][1] - new_centroids[z][1]) < 0.001
                   for z in range(len(self.centroids))):
                break

            self.centroids = new_centroids

        self.cluster_assignments = new_assignments
        return self._get_clusters()

    def _get_clusters(self):
        """Return dict of zone_id -> list of slots"""
        clusters = {z: [] for z in range(self.k)}
        for slot, zone in self.cluster_assignments.items():
            clusters[zone].append(slot)
        return clusters

    def select_target_zone(self, gate):
        """Return zone_id whose centroid is closest to gate"""
        min_dist = float('inf')
        best_zone = 0
        for zone, centroid in enumerate(self.centroids):
            dist = self.manhattan(gate, tuple(centroid))
            if dist < min_dist:
                min_dist = dist
                best_zone = zone
        return best_zone

    def get_zone_slots(self, zone_id):
        """Return list of free slots in given zone"""
        return [s for s, z in self.cluster_assignments.items() if z == zone_id]

    def update_centroids(self, removed_slot):
        """Remove a slot and recompute centroid for its zone"""
        if removed_slot in self.free_slots:
            self.free_slots.remove(removed_slot)

        zone = self.cluster_assignments.get(removed_slot)
        if zone is not None:
            del self.cluster_assignments[removed_slot]
            zones = self._get_clusters()
            if zones[zone]:
                avg_r = sum(s[0] for s in zones[zone]) / len(zones[zone])
                avg_c = sum(s[1] for s in zones[zone]) / len(zones[zone])
                self.centroids[zone] = [avg_r, avg_c]