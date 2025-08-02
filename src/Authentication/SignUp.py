import uuid
import json
from datetime import datetime

LOG_FILE = r"D:\Restaurant_management_system\src\Logs\logs.txt"
path = r"D:\Restaurant_management_system\src\Database\Staff.json"

def write_log(message):
    """Write logs to logs.txt with timestamp."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"[{datetime.now()}] {message}\n")

class SignUp_Menu:
    
    def SignUp_management(self):
        from src.Authentication.ManageMenu import ManageMenu
        staff_List = []

        try:
            # Read existing staff data
            with open(path, "r") as file:
                staff_List = json.load(file)
        except FileNotFoundError:
            print("Staff data file not found. Creating a new one.")
            write_log("Staff.json not found. Creating a new file.")
            staff_List = []
        except json.JSONDecodeError:
            print("Staff data file is empty or corrupted. Resetting file.")
            write_log("ERROR: Staff.json was corrupted or empty. Resetting.")
            staff_List = []
        except Exception as e:
            print("Unexpected error reading staff data.")
            write_log(f"ERROR reading staff.json: {e}")
            return

        try:
            # Take new staff details
            staff_Dict = {}
            staff_id = str(uuid.uuid4())[:6]
            staff_Dict["id"] = staff_id
            staff_Dict["username"] = input("Enter your username: ")
            staff_Dict["email"] = input("Enter your email: ")
            staff_Dict["password"] = input("Enter your password: ")

            # Add to staff list and save
            staff_List.append(staff_Dict)

            with open(path, "w") as file:
                json.dump(staff_List, file, indent=4)

            print("Sign Up successful! You can now log in.")
            write_log(f"New staff registered: {staff_Dict['username']} (ID: {staff_id})")

            # Redirect to MenuManagement
            manage_me = ManageMenu()
            manage_me.MenuManagement()

        except Exception as e:
            print("Error during sign-up process.")
            write_log(f"ERROR during SignUp_management: {e}")
