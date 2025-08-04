import json
import os
import uuid
from datetime import datetime

LOG_FILE = r"D:\Restaurant_management_system\src\Logs\logs.txt"

def write_log(message):
    """Write logs to logs.txt with timestamp."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"[{datetime.now()}] {message}\n")

def admin_menu():
    while True:
        print("\n--- Admin Management ---")
        print("1. View Full Menu")
        print("2. Add Item")
        print("3. Remove Item")
        print("4. Update Item")
        print("5. View Reports")
        print("6. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                write_log("Viewed full menu")
                view_menu()
            elif choice == "2":
                add_item()
            elif choice == "3":
                remove_item()
            elif choice == "4":
                update_item()
            elif choice == "5":
                write_log("Viewed reports section")
                view_reports()
            elif choice == "6":
                print("Exiting Admin Menu...")
                write_log("Exited Admin Menu")
                break
            else:
                print("Please enter a number between 1 to 6.")
                write_log(f"Invalid choice entered: {choice}")
        except Exception as e:
            print("An unexpected error occurred.")
            write_log(f"ERROR in admin_menu: {e}")

def view_menu():
    try:
        with open("src/Database/Menu.json", "r") as file:
            menu = json.load(file)
        if len(menu) == 0:
            print("Menu is empty right now.")
            write_log("Menu viewed but found empty.")
        else:
            print("\n--- Full Menu ---")
            categories = {"Starters": [], "Main Course": [], "Drinks": [], "Desserts": []}

            for item in menu:
                category = item.get("category", "Main Course")
                if category not in categories:
                    category = "Main Course"
                categories[category].append(item)

            for cat, items in categories.items():
                if items:
                    print(f"\n{cat}:")
                    for i in range(len(items)):
                        print(f"  {i+1}. {items[i]['name']} - ₹{items[i]['price']}")
    except FileNotFoundError:
        print("Menu file not found.")
        write_log("ERROR: Menu file not found.")
    except json.JSONDecodeError:
        print("Menu file is empty or broken.")
        write_log("ERROR: Menu file is empty or broken.")
    except Exception as e:
        print("Error while viewing menu.")
        write_log(f"ERROR in view_menu: {e}")

def add_item():
    try:
        name = input("Enter item name: ")
        price = int(input("Enter item price: "))

        print("\nChoose category:")
        print("1. Starters")
        print("2. Main Course")
        print("3. Drinks")
        print("4. Desserts")
        choice = input("Enter category number (1-4): ")

        if choice == "1":
            category = "Starters"
        elif choice == "2":
            category = "Main Course"
        elif choice == "3":
            category = "Drinks"
        elif choice == "4":
            category = "Desserts"
        else:
            print("Invalid choice! Defaulting to 'Main Course'")
            category = "Main Course"

        new_item = {"id": str(uuid.uuid4())[:6], "name": name, "price": price, "category": category}

        try:
            with open("src/Database/Menu.json", "r") as file:
                menu = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            menu = []

        menu.append(new_item)
        with open("src/Database/Menu.json", "w") as file:
            json.dump(menu, file, indent=4)

        print(f"Item '{name}' added under '{category}' category.")
        write_log(f"Added item: {name} (Category: {category}, Price: ₹{price})")

    except ValueError:
        print("Price must be a number.")
        write_log("ERROR: Non-numeric price entered in add_item.")
    except Exception as e:
        print("Error while adding item.")
        write_log(f"ERROR in add_item: {e}")

def remove_item():
    try:
        with open("src/Database/Menu.json", "r") as file:
            menu = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Menu not found.")
        write_log("ERROR: Menu not found during remove_item.")
        return

    if not menu:
        print("Menu is empty.")
        write_log("Tried to remove item but menu is empty.")
        return

    try:
        categories = {"Starters": [], "Main Course": [], "Drinks": [], "Desserts": []}
        category_indexes = {"Starters": [], "Main Course": [], "Drinks": [], "Desserts": []}

        for index, item in enumerate(menu):
            category = item.get("category", "Main Course")
            if category not in categories:
                category = "Main Course"
            categories[category].append(item)
            category_indexes[category].append(index)

        print("\nChoose category to remove from:")
        print("1. Starters")
        print("2. Main Course")
        print("3. Drinks")
        print("4. Desserts")
        cat_choice = input("Enter category number (1-4): ")

        if cat_choice == "1":
            selected_cat = "Starters"
        elif cat_choice == "2":
            selected_cat = "Main Course"
        elif cat_choice == "3":
            selected_cat = "Drinks"
        elif cat_choice == "4":
            selected_cat = "Desserts"
        else:
            print("Invalid category choice.")
            write_log("Invalid category selected in remove_item.")
            return

        items_in_cat = categories[selected_cat]
        indexes_in_cat = category_indexes[selected_cat]

        if not items_in_cat:
            print(f"No items found in {selected_cat}.")
            write_log(f"No items in {selected_cat} to remove.")
            return

        print(f"\n--- {selected_cat} ---")
        for i in range(len(items_in_cat)):
            print(f"{i+1}. {items_in_cat[i]['name']} - ₹{items_in_cat[i]['price']}")

        num = int(input("Enter item number to remove: ")) - 1
        if 0 <= num < len(items_in_cat):
            original_index = indexes_in_cat[num]
            removed_item = menu.pop(original_index)

            with open("src/Database/Menu.json", "w") as file:
                json.dump(menu, file, indent=4)

            print(f"Removed '{removed_item['name']}' from {selected_cat}.")
            write_log(f"Removed item: {removed_item['name']} from {selected_cat}")
        else:
            print("Invalid item number.")
            write_log("Invalid item number in remove_item.")
    except ValueError:
        print("Enter a valid number.")
        write_log("ERROR: Non-numeric input in remove_item.")
    except Exception as e:
        print("Error while removing item.")
        write_log(f"ERROR in remove_item: {e}")

def update_item():
    try:
        with open("src/Database/Menu.json", "r") as file:
            menu = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Menu not found.")
        write_log("ERROR: Menu not found during update_item.")
        return

    if not menu:
        print("Menu is empty.")
        write_log("Tried to update item but menu is empty.")
        return

    try:
        categories = {"Starters": [], "Main Course": [], "Drinks": [], "Desserts": []}
        category_indexes = {"Starters": [], "Main Course": [], "Drinks": [], "Desserts": []}

        for index, item in enumerate(menu):
            category = item.get("category", "Main Course")
            if category not in categories:
                category = "Main Course"
            categories[category].append(item)
            category_indexes[category].append(index)

        print("\nChoose category to update from:")
        print("1. Starters")
        print("2. Main Course")
        print("3. Drinks")
        print("4. Desserts")
        cat_choice = input("Enter category number (1-4): ")

        if cat_choice == "1":
            selected_cat = "Starters"
        elif cat_choice == "2":
            selected_cat = "Main Course"
        elif cat_choice == "3":
            selected_cat = "Drinks"
        elif cat_choice == "4":
            selected_cat = "Desserts"
        else:
            print("Invalid category choice.")
            write_log("Invalid category selected in update_item.")
            return

        items_in_cat = categories[selected_cat]
        indexes_in_cat = category_indexes[selected_cat]

        if not items_in_cat:
            print(f"No items found in {selected_cat}.")
            write_log(f"No items in {selected_cat} to update.")
            return

        print(f"\n--- {selected_cat} ---")
        for i in range(len(items_in_cat)):
            print(f"{i+1}. {items_in_cat[i]['name']} - ₹{items_in_cat[i]['price']}")

        num = int(input("Enter item number to update: ")) - 1
        if 0 <= num < len(items_in_cat):
            original_index = indexes_in_cat[num]

            new_name = input("Enter new name (leave blank to keep same): ")
            new_price = input("Enter new price (leave blank to keep same): ")

            print("\nChoose new category (leave blank to keep same):")
            print("1. Starters")
            print("2. Main Course")
            print("3. Drinks")
            print("4. Desserts")
            new_cat_choice = input("Enter category number or press Enter: ")

            if new_name:
                menu[original_index]['name'] = new_name
            if new_price:
                menu[original_index]['price'] = int(new_price)
            if new_cat_choice == "1":
                menu[original_index]['category'] = "Starters"
            elif new_cat_choice == "2":
                menu[original_index]['category'] = "Main Course"
            elif new_cat_choice == "3":
                menu[original_index]['category'] = "Drinks"
            elif new_cat_choice == "4":
                menu[original_index]['category'] = "Desserts"

            with open("src/Database/Menu.json", "w") as file:
                json.dump(menu, file, indent=4)

            print("Item updated successfully.")
            write_log(f"Updated item: {menu[original_index]['name']}")
        else:
            print("Invalid item number.")
            write_log("Invalid item number in update_item.")
    except ValueError:
        print("Enter valid input.")
        write_log("ERROR: Non-numeric input in update_item.")
    except Exception as e:
        print("Error while updating item.")
        write_log(f"ERROR in update_item: {e}")

    write_log("Viewed report section.")
    

def view_reports():
    bill_file = r"D:\Restaurant_management_system\src\Database\Bill.json"
    
    if not os.path.exists(bill_file):
        print("No sales data found (Bill.json missing).")
        return

    try:
        with open(bill_file, "r") as file:
            bills = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        print("Error reading sales data.")
        return

    if not bills:
        print("No sales records available.")
        return

    today = datetime.now().date()
    todays_bills = [
        bill for bill in bills 
        if bill.get("date") and datetime.strptime(bill["date"], "%Y-%m-%d %H:%M:%S").date() == today
    ]

    if not todays_bills:
        print("No sales recorded today.")
        return

    total_orders = len(todays_bills)
    total_sales = sum(bill["total_amount"] for bill in todays_bills)

    from collections import Counter
    item_list = []
    for bill in todays_bills:
        for item in bill.get("items", []): 
            item_list.append(item["name"])

    if item_list:
        most_common_item, qty = Counter(item_list).most_common(1)[0]
    else:
        most_common_item, qty = None, 0

    print("\n--- Daily Sales Report ---")
    print(f"Date: {today}")
    print(f"Total Orders Today: {total_orders}")
    print(f"Total Sales Amount Today: ₹{total_sales:.2f}")
    if most_common_item:
        print(f"Top Selling Item: {most_common_item} (Sold {qty} times)")
    else:
        print("Top Selling Item: No items sold today.")
