from controller import Controller
from input_handler import InputHandler
from parking_grid import ParkingGrid
from a_star_search import AStarSearch
from console_visualizer import ConsoleVisualizer

def main():
    while True:
        print("\n" + "="*50)
        print("SMART PARKING SYSTEM - CONSOLE MODE")
        print("="*50)
        print("1. Run interactive console mode")
        print("2. Run automated test suite")
        print("3. Exit")
        print("-"*50)
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            # Interactive mode
            handler = InputHandler()
            params = handler.get_grid_params()
            
            # Create parking grid first
            rows = params['rows']
            cols = params['cols']
            gate = params['gate']
            occ = params['occupancy']
            
            print("\n" + "="*50)
            print("INITIAL PARKING GRID")
            print("="*50)
            
            parking_grid = ParkingGrid(rows, cols, gate, occ)
            visualizer = ConsoleVisualizer(parking_grid)
            visualizer.render()
            
            print("\n" + "="*50)
            print("ALLOCATING CARS")
            print("="*50)
            
            ctrl = Controller.get_instance()
            ctrl.run(params, mode='cli', num_cars=params.get('num_cars', 3))
            
            print("\n=== RESULTS ===")
            print(f"Cars parked: {ctrl.num_cars_parked}")
            for i, path in enumerate(ctrl.all_paths):
                print(f"Car {i+1}: path length {len(path)-1} moves")
                print(f"  Path: {path}")
            
            if hasattr(ctrl, 'visualizer') and ctrl.visualizer:
                print("\n" + "="*50)
                print(f"FINAL GRID AFTER {ctrl.num_cars_parked} CAR(S) PARKED")
                print("="*50)
                ctrl.visualizer.render()
            
            input("\nPress Enter to return to menu...")
        
        elif choice == "2":
            # Test suite mode - with grid display for each test
            print("\n" + "="*60)
            print("CORE A* ALGORITHM VALIDATION")
            print("="*60)
            
            test_cases = [
                {"rows": 5, "cols": 5, "gate": (1,0), "occ": 30, "name": "Basic 5x5 Grid"},
                {"rows": 7, "cols": 7, "gate": (1,0), "occ": 80, "name": "High Occupancy 7x7"},
                {"rows": 5, "cols": 5, "gate": (3,2), "occ": 30, "name": "Gate at Bottom Middle"},
            ]
            
            for i, test in enumerate(test_cases, 1):
                print(f"\n{'='*60}")
                print(f"TEST {i}: {test['name']}")
                print(f"Grid: {test['rows']}x{test['cols']}, Gate: {test['gate']}, Occupancy: {test['occ']}%")
                print('='*60)
                
                # Show initial grid
                parking_grid = ParkingGrid(test['rows'], test['cols'], test['gate'], test['occ'])
                visualizer = ConsoleVisualizer(parking_grid)
                visualizer.render()
                
                # Run A*
                searcher = AStarSearch(parking_grid)
                goal = searcher.search(test['gate'], set())
                
                print(f"\n--- SEARCH RESULT ---")
                if goal:
                    path = searcher.reconstruct_path(goal)
                    print(f"✓ Path found to ({goal.row}, {goal.col})")
                    print(f"  Path cost: {len(path)-1} moves")
                    print(f"  Path: {path}")
                else:
                    print("✗ No path found")
                
                print("-"*40)
            
            print("\n" + "="*60)
            print("ALL TESTS COMPLETED")
            print("="*60)
            input("\nPress Enter to return to menu...")
        
        elif choice == "3":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()