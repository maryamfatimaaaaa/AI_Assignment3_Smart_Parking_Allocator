# Smart Parking System

AI-driven smart parking slot allocation using A* Search and K-Means Zone Clustering.

**Course:** AI2002 Artificial Intelligence
**Semester:** Spring 2026
**Group Members:**
- Syed Sheharyar Ali (23i-0097)
- Muhammad Ali Sajjad (23i-0110)
- Maryam Fatima (23i-3007)

---

## Project Overview

The Smart Parking System assigns parking slots to incoming vehicles using two AI techniques:

1. **A* Search Algorithm** — finds the shortest path from the entry gate to the nearest available parking slot using Manhattan distance as the heuristic
2. **K-Means Zone Clustering** — partitions the parking grid into K spatial zones before invoking A*, restricting the search to the nearest zone and reducing the effective search space from O(R x C) to O(R x C / K)

The system supports both a Streamlit web GUI and a console CLI interface.

---

## File Structure

```
SmartParking/
    main.py                   Entry point. Detects runtime mode and launches GUI or CLI.
    controller.py             Singleton Controller. Orchestrates full pipeline.
    search_algorithm.py       Abstract base class for search algorithms (Strategy Pattern).
    a_star_search.py          Concrete A* Search implementation.
    k_means_clusterer.py      K-Means clustering for zone partitioning.
    parking_grid.py           Grid construction, occupancy, adjacency graph.
    cell.py                   Cell data class used in display grid.
    node.py                   Node class used by A* (row, col, g, h, f, parent).
    min_heap.py               Min-heap priority queue for A* open list.
    visualizer.py             Abstract base Visualizer (Template Method Pattern).
    console_visualizer.py     Console/CLI rendering with ASCII grid.
    streamlit_visualizer.py   Streamlit GUI rendering with Matplotlib.
    input_handler.py          User input collection and validation.
    requirements.txt          Python dependencies.
    README.md                 This file.
    How To Run.txt            Quick-start instructions.
```

---

## Requirements

- Python 3.10 or higher
- streamlit >= 1.28.0
- numpy >= 1.24.0
- matplotlib >= 3.7.0
- pandas >= 2.0.0

---

## Installation and Running

### Streamlit GUI

```bash
cd SmartParking
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / macOS
pip install -r requirements.txt
streamlit run main.py
```

### Console CLI

```bash
python main.py --console
```

---

## How It Works

### Grid Structure

The system builds a logical R x C grid where alternating rows are road lanes and parking rows. This is expanded into a display grid of size (2R+1) x (C+2) for rendering and path computation.

### A* Search

A* evaluates each node using:

```
f(n) = g(n) + h(n)
```

where g(n) is the exact cost from the gate to the current node and h(n) is the Manhattan distance to the nearest free slot. The open list is managed by a min-heap ordered by f(n).

### K-Means Zone Clustering

Before each A* invocation, free slots are clustered into K zones. The zone whose centroid is closest to the gate is selected and A* searches only within that zone. If the zone is empty, the system falls back to the full grid.

### Multi-Car Allocation

Cars are allocated sequentially. After each allocation the assigned slot is added to a reserved set and the K-Means centroids are updated. The next car then runs A* against the updated zone structure.

---

## Design Patterns Used

| Pattern | Where Applied |
|---|---|
| Singleton | Controller — only one instance via get_instance() |
| Strategy | SearchAlgorithm abstract base, AStarSearch as concrete strategy |
| Template Method | Visualizer abstract base, ConsoleVisualizer and StreamlitVisualizer as concrete renderers |

---

## Optimization Strategies

1. Duplicate node avoidance via closed list
2. Early termination when goal is found
3. Weighted occupancy initialization (slots near gate fill first)
4. O(1) slot lookup using Python sets
5. Zone-restricted search via K-Means (search space reduced by factor K)
6. Heuristic precomputation and caching (O(1) lookup per node expansion)

---

## Test Cases

| Test | Grid | Occupancy | Cars | Result |
|---|---|---|---|---|
| Basic | 5x5 | 30% | 1 | Slot found in 3 nodes |
| Multi-car | 7x7 | 50% | 3 | All 3 cars allocated |
| Edge case | 3x3 | 80% | 5 | 1 car parked, 4 not accommodated |

---

## Limitations

- Occupancy capped at 80%
- Grid is randomly regenerated each run (no fixed seed by default)
- All cars depart from a single gate sequentially
- No car queuing when all slots are full
