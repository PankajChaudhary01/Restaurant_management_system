import json
from datetime import datetime
from src.Domain.Admin.AdminMenu import admin_menu  
from src.Domain.Staff.StaffMenu import staff_menu

LOG_FILE = r"D:\Restaurant_management_system\src\Logs\logs.txt"

def write_log(message):
    """Write logs to logs.txt with timestamp."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"[{datetime.now()}] {message}\n")

class SignIn:
    
    def admin_login(self):
        try:
            with open('src/Database/admin.json', 'r') as file:
                admin_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Admin data not found or invalid.")
            write_log("ERROR: Admin data file not found or invalid.")
            return

        try:
            username = input("Enter admin username: ")
            password = input("Enter admin password: ")

            for admin in admin_data:
                if admin["username"] == username and admin["password"] == password:
                    print("Admin login successful!\n")
                    write_log(f"Admin login successful (username: {username})")
                    admin_menu()
                    return  

            print("Invalid admin credentials.\n")
            write_log(f"Failed admin login attempt (username: {username})")
        except Exception as e:
            print("An unexpected error occurred during admin login.")
            write_log(f"ERROR in admin_login: {e}")

    def staff_login(self):
        try:
            with open('src/Database/Staff.json', 'r') as file:
                staff_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Staff data not found or invalid.")
            write_log("ERROR: Staff data file not found or invalid.")
            return

        try:
            username = input("Enter staff username: ")
            password = input("Enter staff password: ")

            for staff in staff_data:
                if staff["username"] == username and staff["password"] == password:
                    print("Staff login successful!\n")
                    write_log(f"Staff login successful (username: {username})")
                    staff_menu()
                    return

            print("Invalid staff credentials.\n")
            write_log(f"Failed staff login attempt (username: {username})")
        except Exception as e:
            print("An unexpected error occurred during staff login.")
            write_log(f"ERROR in staff_login: {e}")

    def sign_in_menu(self):
        while True:
            try:
                print("\n--- Sign In Menu ---")
                print("1. Admin Login")
                print("2. Staff Login")
                print("3. Exit")

                choice = input("Enter your choice: ")

                if choice == '1':
                    write_log("User selected Admin Login.")
                    self.admin_login()
                elif choice == '2':
                    write_log("User selected Staff Login.")
                    self.staff_login()
                elif choice == '3':
                    print("Returning to main menu.")
                    write_log("User exited Sign In Menu.")
                    break
                else:
                    print("Invalid input. Please enter 1, 2, or 3.\n")
                    write_log(f"Invalid Sign In menu choice entered: {choice}")
            except Exception as e:
                print("An unexpected error occurred in Sign In Menu.")
                write_log(f"ERROR in sign_in_menu: {e}")
