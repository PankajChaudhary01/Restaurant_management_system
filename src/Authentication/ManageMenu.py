from src.Authentication.SignUp import SignUp_Menu
from src.Authentication.SignIn import SignIn
from datetime import datetime

LOG_FILE = r"D:\Restaurant_management_system\src\Logs\logs.txt"

def write_log(message):
    """Write logs to logs.txt with timestamp."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"[{datetime.now()}] {message}\n")

class ManageMenu:
    def MenuManagement(self):
        try:
            print("--* Pankaj's Restaurant *--")
            print("1. Sign in")
            print("2. Sign up")
            print("3. Exit")

            choice = int(input("Enter your choice: "))

            if choice == 1:
                write_log("User selected Sign In")
                login = SignIn()
                try:
                    login.sign_in_menu()
                    write_log("Sign In process completed successfully.")
                except Exception as e:
                    print("Error during Sign In.")
                    write_log(f"ERROR during Sign In: {e}")

            elif choice == 2:
                write_log("User selected Sign Up")
                signup = SignUp_Menu()
                try:
                    signup.SignUp_management()
                    write_log("Sign Up process completed successfully.")
                except Exception as e:
                    print("Error during Sign Up.")
                    write_log(f"ERROR during Sign Up: {e}")

            elif choice == 3:
                print("Thank you for visiting us")
                write_log("User exited the program.")
                exit()

            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
                write_log(f"Invalid choice entered: {choice}")

        except ValueError:
            print("Please enter a valid number.")
            write_log("ERROR: Non-numeric input entered in MenuManagement.")
        except Exception as e:
            print("An unexpected error occurred.")
            write_log(f"ERROR in MenuManagement: {e}")
