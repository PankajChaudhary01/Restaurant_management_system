
import json
from src.Domain.Staff.order import OrderSystem
def staff_menu():
        while True:
            print("\n--- Staff Menu ---")
            print("1. View Full Menu")
            print("2. Process Order")
            print("3. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
               
                view_menu()
                


            elif choice == "2":
                print("\n--- Order processing ---")
                Order=OrderSystem()
                Order.process()

            elif choice == "3":
                print("Exiting Staff Menu")
                break

            else:
                print("Invalid choice! Please try again.")
                
def view_menu():
    try:
        with open("src/Database/Menu.json", "r") as file:
            menu = json.load(file)
    except FileNotFoundError:
        print("Menu file not found.")
        return
    except json.JSONDecodeError:
        print("Menu file is empty or broken.")
        return

    if len(menu) == 0:
        print("Menu is empty right now.")
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
