import json
from src.Domain.Admin.AdminMenu import admin_menu  
from src.Domain.Staff.StaffMenu import staff_menu
class SignIn:
    
    def admin_login(self):
        try:
            with open('src/Database/admin.json', 'r') as file:
                admin_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Admin data not found or invalid.")
            return

        username = input("Enter admin username: ")
        password = input("Enter admin password: ")

        for admin in admin_data:
            if admin["username"] == username and admin["password"] == password:
                print("Admin login successful!\n")
                admin_menu()
                return  
        print("Invalid admin credentials.\n")
    
    
    def staff_login(self):
        try:
            with open('src/Database/Staff.json', 'r') as file:
                staff_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Staff data not found or invalid.")
            return

        username = input("Enter staff username: ")
        password = input("Enter staff password: ")

        for staff in staff_data:
            if staff["username"] == username and staff["password"] == password:
                print("Staff login successful!\n")
                staff_menu()
                return
        print("Invalid staff credentials.\n")

    def sign_in_menu(self):
        while True:
            print("\n--- Sign In Menu ---")
            print("1. Admin Login")
            print("2. Staff Login")
            print("3. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.admin_login()
            elif choice == '2':
                self.staff_login()
            elif choice == '3':
                break
            else:
                print("Invalid input. Please enter 1, 2, or 3.\n")
