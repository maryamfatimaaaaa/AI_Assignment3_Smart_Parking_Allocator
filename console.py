from controller import Controller
from input_handler import InputHandler
from parking_grid import ParkingGrid
from a_star_search import AStarSearch

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
            ctrl = Controller.get_instance()
            ctrl.run(params, mode='cli', num_cars=params.get('num_cars', 3))
            
            print("\n=== RESULTS ===")
            print(f"Cars parked: {ctrl.num_cars_parked}")
            for i, path in enumerate(ctrl.all_paths):
                print(f"Car {i+1}: path length {len(path)-1} moves")
            
            if hasattr(ctrl, 'visualizer') and ctrl.visualizer:
                ctrl.visualizer.render()
            
            input("\nPress Enter to return to menu...")
        
        elif choice == "2":
            # Test suite mode
            print("\n" + "="*60)
            print("CORE A* ALGORITHM VALIDATION")
            print("="*60)
            
            test_cases = [
                {"rows": 5, "cols": 5, "gate": (1,0), "occ": 30},
                {"rows": 7, "cols": 7, "gate": (1,0), "occ": 80},
                {"rows": 5, "cols": 5, "gate": (3,2), "occ": 30},
            ]
            
            for i, test in enumerate(test_cases, 1):
                print(f"\nTest {i}: {test['rows']}x{test['cols']}, Gate {test['gate']}, {test['occ']}%")
                print("-" * 40)
                
                grid = ParkingGrid(test['rows'], test['cols'], test['gate'], test['occ'])
                searcher = AStarSearch(grid)
                goal = searcher.search(test['gate'], set())
                
                if goal:
                    path = searcher.reconstruct_path(goal)
                    print(f"Path found to ({goal.row}, {goal.col})")
                    print(f"Path cost: {len(path)-1}")
                else:
                    print("No path found")
            
            print("\n" + "="*60)
            input("\nPress Enter to return to menu...")
        
        elif choice == "3":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()