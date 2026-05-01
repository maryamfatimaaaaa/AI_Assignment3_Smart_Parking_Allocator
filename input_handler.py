# input_handler.py

class InputHandler:
    @staticmethod
    def get_grid_params():
        """Collect grid parameters from console input including number of cars"""
        print("***************************************")
        print("*        SMART PARKING SYSTEM         *")
        print("***************************************\n")

        print("Welcome to Smart Parking System\n")
        print("*****************************")
        print("*       USER INPUT          *")
        print("*****************************")

        # Rows
        while True:
            rows_input = input("Enter number of rows for grid: ")
            if rows_input.isdigit() and int(rows_input) > 1:
                rows = int(rows_input)
                break
            print("Rows must be greater than 1.")

        # Columns
        while True:
            cols_input = input("Enter number of columns for grid: ")
            if cols_input.isdigit() and int(cols_input) > 1:
                cols = int(cols_input)
                break
            print("Columns must be greater than 1.")

        # Gate
        print("\nGate must be placed on the border of grid.")
        while True:
            gr_input = input(f"Enter gate row position (0 to {rows-1}): ")
            gc_input = input(f"Enter gate column position (0 to {cols-1}): ")
            if gr_input.isdigit() and gc_input.isdigit():
                gr, gc = int(gr_input), int(gc_input)
                if 0 <= gr < rows and 0 <= gc < cols:
                    if gr == 0 or gr == rows-1 or gc == 0 or gc == cols-1:
                        gate_row, gate_col = gr, gc
                        break
            print("Gate must be on border of grid.")

        # Occupancy
        print("\nMaximum allowed occupancy is 80%.")
        while True:
            occ_input = input("Enter percentage of occupied parking (0-80): ")
            if occ_input.isdigit() and 0 <= int(occ_input) <= 80:
                occ = int(occ_input)
                break
            print("Percentage must be between 0 and 80.")

        # Number of cars (ADD THIS SECTION)
        print("\nMaximum 10 cars can enter at once.")
        while True:
            cars_input = input("Enter number of cars entering: ")
            if cars_input.isdigit() and 1 <= int(cars_input) <= 10:
                num_cars = int(cars_input)
                break
            print("Number of cars must be between 1 and 10.")

        return {
            'rows': rows,
            'cols': cols,
            'gate': (gate_row, gate_col),
            'occupancy': occ,
            'num_cars': num_cars   # Added
        }

    @staticmethod
    def validate(params):
        """Validate grid parameters"""
        rows = params.get('rows', 0)
        cols = params.get('cols', 0)
        gate = params.get('gate', (0, 0))
        occ = params.get('occupancy', 0)

        if rows < 3 or rows > 15:
            return False
        if cols < 3 or cols > 15:
            return False
        if not (gate[0] == 0 or gate[0] == rows-1 or gate[1] == 0 or gate[1] == cols-1):
            return False
        if occ < 0 or occ > 80:
            return False
        return True