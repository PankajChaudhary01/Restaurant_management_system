import json
import os
import uuid
from datetime import datetime

class TableBooking:
    def __init__(self):
        self.database_dir = r"D:\Restaurant_management_system\src\Database"
        os.makedirs(self.database_dir, exist_ok=True)

        self.booking_file = os.path.join(self.database_dir, "Table.json")
        self.tables_config_file = os.path.join(self.database_dir, "tables_config.json")

        # Load tables configuration or create default
        self.tables_data = self._load_or_create_config()
        # Load existing bookings
        self.table_bookings = self._load_json_file(self.booking_file, "booking data", default_value=[])

    def _load_or_create_config(self):
        """Load table configuration or auto-create default if missing/broken."""
        if not os.path.exists(self.tables_config_file):
            print(f"'{self.tables_config_file}' missing. Creating default table config.")
            default_config = [
                {"table_no": 1, "total_seats": 4},
                {"table_no": 2, "total_seats": 2},
                {"table_no": 3, "total_seats": 6}
            ]
            with open(self.tables_config_file, 'w') as file:
                json.dump(default_config, file, indent=4)
            return default_config
        try:
            with open(self.tables_config_file, 'r') as file:
                data = json.load(file)
                if isinstance(data, list) and data:
                    return data
                else:
                    print("Invalid or empty config detected. Recreating default config.")
                    return self._create_default_config()
        except (json.JSONDecodeError, FileNotFoundError):
            print("Error reading config. Recreating default config.")
            return self._create_default_config()

    def _create_default_config(self):
        default_config = [
            {"table_no": 1, "total_seats": 4},
            {"table_no": 2, "total_seats": 2},
            {"table_no": 3, "total_seats": 6}
        ]
        with open(self.tables_config_file, 'w') as file:
            json.dump(default_config, file, indent=4)
        return default_config

    def _load_json_file(self, file_path, file_description, default_value=None):
        """Safe loader for JSON files, auto-initializes if missing/corrupt."""
        if default_value is None:
            default_value = []
        if not os.path.exists(file_path):
            print(f"ℹ️ {file_description.capitalize()} file missing. Creating empty.")
            with open(file_path, 'w') as file:
                json.dump(default_value, file)
            return default_value
        try:
            with open(file_path, 'r') as file:
                content = file.read().strip()
                if not content:  
                    print(f"{file_description.capitalize()} is empty. Initializing default.")
                    return default_value
                return json.loads(content)
        except json.JSONDecodeError:
            print(f"Corrupted {file_description}. Resetting to default.")
            return default_value

    def save_bookings(self):
        """Save bookings to Table.json"""
        with open(self.booking_file, 'w') as file:
            json.dump(self.table_bookings, file, indent=4, default=str)

    def book_table(self):
        """Book a table by selecting table number and seats."""
        print("\n--- Table Booking ---")

        # Show available tables
        print("\nAvailable Tables:")
        for table in self.tables_data:
            print(f"Table {table['table_no']} - Seats: {table['total_seats']}")

        # Ask for table number
        try:
            table_no = int(input("Enter table number to book: "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            return

    
        selected_table = None
        for table in self.tables_data:
            if table["table_no"] == table_no:
                selected_table = table
                break

        if not selected_table:
            print("Table not found!")
            return

    
        try:
            seats = int(input(f"Enter seats to book (1-{selected_table['total_seats']}): "))
            if seats < 1 or seats > selected_table['total_seats']:
                print("Invalid number of seats!")
                return
        except ValueError:
            print("Invalid input! Please enter a number.")
            return

        
        booking_id = str(uuid.uuid4())[:6]
        booking = {
            "booking_id": booking_id,
            "date": str(datetime.now().date()),
            "time": datetime.now().strftime("%H:%M"),
            "table_no": table_no,
            "seats_booked": seats
        }

        self.table_bookings.append(booking)
        self.save_bookings()

        print(f"Table {table_no} booked successfully for {seats} seats. Booking ID: {booking_id}")
