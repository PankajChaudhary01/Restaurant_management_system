import json
import datetime
from src.Domain.Staff.order import OrderSystem

LOG_FILE = r"D:\Restaurant_management_system\src\Logs\logs.txt"

def write_log(message):
    """Write logs to logs.txt with timestamp."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"[{datetime.datetime.now()}] {message}\n")

def staff_menu():
    while True:
        print("\n--- Staff Menu ---")
        print("1. View Full Menu")
        print("2. Process Order")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            try:
                view_menu()
                write_log("Staff viewed full menu.")
            except Exception as e:
                print("Error displaying menu.")
                write_log(f"ERROR in viewing menu: {e}")

        elif choice == "2":
            print("\n--- Order processing ---")
            try:
                Order = OrderSystem()
                Order.process()
                write_log("Staff initiated order processing.")
            except Exception as e:
                print("Error during order processing.")
                write_log(f"ERROR in order processing: {e}")

        elif choice == "3":
            print("Exiting Staff Menu")
            write_log("Staff exited menu.")
            break

        else:
            print("Invalid choice! Please try again.")
            write_log(f"Invalid staff menu choice entered: {choice}")

def view_menu():
    try:
        with open("src/Database/Menu.json", "r") as file:
            menu = json.load(file)
    except FileNotFoundError:
        print("Menu file not found.")
        write_log("ERROR: Menu file not found.")
        return
    except json.JSONDecodeError:
        print("Menu file is empty or broken.")
        write_log("ERROR: Menu file is empty/corrupted.")
        return

    if len(menu) == 0:
        print("Menu is empty right now.")
        write_log("Menu viewed but found empty.")
    else:
        print("\n--- Full Menu ---")
        categories = {
            "Starters": [],
            "Main Course": [],
            "Drinks": [],
            "Desserts": []
        }

        for item in menu:
            category = item.get("category", "Main Course")
            if category not in categories:
                category = "Main Course"
            categories[category].append(item)

        for cat, items in categories.items():
            if items:
                print(f"\n{cat}:")
                for i, item in enumerate(items, start=1):
                    print(f"  {i}. {item['name']} - ₹{item['price']}")
        write_log("Menu displayed successfully.")
