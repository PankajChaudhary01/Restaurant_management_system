import json
import os
import uuid
from datetime import datetime

LOG_FILE = r"D:\Restaurant_management_system\src\Logs\logs.txt"

def write_log(message):
    """Write logs to logs.txt with timestamp."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"[{datetime.now()}] {message}\n")

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
        try:
            if not os.path.exists(self.tables_config_file):
                print(f"'{self.tables_config_file}' missing. Creating default table config.")
                write_log("Table config file missing. Creating default.")
                return self._create_default_config()

            with open(self.tables_config_file, 'r') as file:
                data = json.load(file)
                if isinstance(data, list) and data:
                    return data
                else:
                    print("Invalid or empty config detected. Recreating default config.")
                    write_log("Invalid or empty table config detected. Recreating.")
                    return self._create_default_config()

        except (json.JSONDecodeError, FileNotFoundError):
            print("Error reading config. Recreating default config.")
            write_log("ERROR: Corrupted/missing table config. Recreated.")
            return self._create_default_config()

    def _create_default_config(self):
        default_config = [
            {"table_no": 1, "total_seats": 4},
            {"table_no": 2, "total_seats": 2},
            {"table_no": 3, "total_seats": 6}
        ]
        with open(self.tables_config_file, 'w') as file:
            json.dump(default_config, file, indent=4)
        write_log("Default table config created.")
        return default_config

    def _load_json_file(self, file_path, file_description, default_value=None):
        """Safe loader for JSON files, auto-initializes if missing/corrupt."""
        if default_value is None:
            default_value = []
        try:
            if not os.path.exists(file_path):
                print(f"{file_description.capitalize()} file missing. Creating empty.")
                write_log(f"{file_description.capitalize()} file missing. Created new empty file.")
                with open(file_path, 'w') as file:
                    json.dump(default_value, file)
                return default_value

            with open(file_path, 'r') as file:
                content = file.read().strip()
                if not content:  
                    print(f"{file_description.capitalize()} is empty. Initializing default.")
                    write_log(f"{file_description.capitalize()} is empty. Initialized default.")
                    return default_value
                return json.loads(content)
        except json.JSONDecodeError:
            print(f"Corrupted {file_description}. Resetting to default.")
            write_log(f"ERROR: Corrupted {file_description}. Reset to default.")
            return default_value

    def save_bookings(self):
        """Save bookings to Table.json"""
        try:
            with open(self.booking_file, 'w') as file:
                json.dump(self.table_bookings, file, indent=4, default=str)
            write_log("Table bookings saved successfully.")
        except Exception as e:
            print("Failed to save table bookings.")
            write_log(f"ERROR saving table bookings: {e}")

    def book_table(self):
        """Book a table by selecting table number and seats."""
        print("\n--- Table Booking ---")

        # Show available tables
        print("\nAvailable Tables:")
        for table in self.tables_data:
            print(f"Table {table['table_no']} - Seats: {table['total_seats']}")

        try:
            # Ask for table number
            table_no = int(input("Enter table number to book: "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            write_log("Invalid table number input.")
            return

        selected_table = next((table for table in self.tables_data if table["table_no"] == table_no), None)
        if not selected_table:
            print("Table not found!")
            write_log(f"Attempted booking on non-existent table {table_no}.")
            return

        try:
            seats = int(input(f"Enter seats to book (1-{selected_table['total_seats']}): "))
            if seats < 1 or seats > selected_table['total_seats']:
                print("Invalid number of seats!")
                write_log(f"Invalid seat count {seats} for Table {table_no}.")
                return
        except ValueError:
            print("Invalid input! Please enter a number.")
            write_log("Invalid seat input (non-numeric).")
            return

        try:
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
            write_log(f"Table {table_no} booked successfully for {seats} seats. Booking ID: {booking_id}")
        except Exception as e:
            print("Error occurred during table booking.")
            write_log(f"ERROR during table booking: {e}")
