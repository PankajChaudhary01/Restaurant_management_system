import json
import os
import uuid
import datetime
from src.Domain.Admin.AdminMenu import view_menu
from src.Domain.Bill.Billing import Bills
from src.Domain.Booking.Table import TableBooking

LOG_FILE = r"D:\Restaurant_management_system\src\Logs\logs.txt"

def write_log(message):
    """Write logs to logs.txt with timestamp."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"[{datetime.datetime.now()}] {message}\n")

class OrderSystem:
    def __init__(self):
        self.order_file = r"D:\Restaurant_management_system\src\Database\Order.json"
        self.order = self.load_orders()

    def load_orders(self):  
        """Load existing orders from JSON."""
        if os.path.exists(self.order_file):
            try:
                with open(self.order_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                write_log("ERROR: Order file corrupted or missing. Starting fresh.")
                return []
        return []

    def save_orders(self):
        """Save current orders to JSON."""
        try:
            with open(self.order_file, "w") as f:
                json.dump(self.order, f, indent=4)
            write_log("Orders saved successfully.")
        except Exception as e:
            print("Failed to save orders.")
            write_log(f"ERROR saving orders: {e}")

    def append_to_file(self, filepath, data):
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as file:
                    existing = json.load(file)
            else:
                existing = []
        except json.JSONDecodeError:
            existing = []
            write_log("WARNING: Order file corrupted. Resetting to empty.")

        existing.append(data)
        try:
            with open(filepath, 'w') as file:
                json.dump(existing, file, indent=4)
            write_log(f"Order appended to {filepath}.")
        except Exception as e:
            print("Failed to append order.")
            write_log(f"ERROR appending order: {e}")

    def add_item(self):
        view_menu()
        try:
            with open("src/Database/Menu.json", "r") as file:
                menu = json.load(file)
        except FileNotFoundError:
            print("Menu file not found.")
            write_log("ERROR: Menu file not found.")
            return
        except json.JSONDecodeError:
            print("Menu file is empty or broken.")
            write_log("ERROR: Menu file corrupted.")
            return

        name = input("\nEnter item name to add: ").strip().lower()
        found = False

        for item in menu:
            if item["name"].lower() == name:
                try:
                    quantity = int(input(f"Enter quantity for {item['name']}: "))
                    if quantity <= 0:
                        print("Quantity must be at least 1.")
                        write_log(f"Invalid quantity {quantity} entered for {item['name']}.")
                        return
                except ValueError:
                    print("Invalid quantity. Please enter a number.")
                    write_log("Non-numeric quantity entered.")
                    return

                order_item = {
                    "name": item["name"],
                    "category": item["category"],
                    "price": int(item["price"]),
                    "quantity": quantity,
                    "total_price": int(item["price"]) * quantity
                }
                self.order.append(order_item)
                self.save_orders()
                print(f"Added: {item['name']} x {quantity}")
                write_log(f"Item added: {item['name']} x{quantity}")
                found = True
                break

        if not found:
            print("Item not found in the menu.")
            write_log(f"Attempted to add unavailable item: {name}")

    def remove_item(self):
        if not self.order:
            print("No items in your order to remove.")
            write_log("Attempted item removal with empty order.")
            return

        print("\n--- Current Order ---")
        for i, item in enumerate(self.order, start=1):
            print(f"{i}. {item['name']} x {item['quantity']} - ₹{item['total_price']}")

        try:
            index = int(input("Enter item number to remove: "))
            if 1 <= index <= len(self.order):
                removed = self.order.pop(index - 1)
                self.save_orders()
                print(f"Removed: {removed['name']}")
                write_log(f"Removed item: {removed['name']}")
            else:
                print("Invalid index.")
                write_log(f"Invalid removal index: {index}")
        except ValueError:
            print("Please enter a valid number.")
            write_log("Non-numeric removal index entered.")

    def finalize_order(self):
        if not self.order:
            print("No items in order.")
            write_log("Finalize attempted on empty order.")
            return

        print("\nSelect Order Type:")
        print("1. Pack Order")
        print("2. Table Booking")
        order_type = input("Enter choice (1 or 2): ").strip()

        if order_type == "2":
            tabBook = TableBooking()
            tabBook.book_table()
            write_log("Table booking initiated during order finalization.")
        elif order_type != "1":
            print("Invalid choice. Cancelling billing.")
            write_log(f"Invalid order type selected: {order_type}")
            return

        print("\n--- Final Order ---")
        print(f"{'Name':<20} {'Qty':<4} {'Unit Price':<10} {'Total':<8}")
        print("-" * 60)
        for item in self.order:
            print(f"{item['name']:<20} {item['quantity']:<4} ₹{item['price']:<10} ₹{item['total_price']:<8}")

        subtotal = sum(item['total_price'] for item in self.order)
        tax = round(subtotal * 0.05, 2)
        discount = round(subtotal * 0.10, 2) if subtotal >= 500 else 0
        total = round(subtotal + tax - discount, 2)

        print(f"\nSubtotal: ₹{subtotal}")
        print(f"Tax (5%): ₹{tax}")
        if discount > 0:
            print(f"Discount (10%): -₹{discount}")
        print(f"Total Amount: ₹{total}")
        print("Please proceed to payment...")

        order_id = str(uuid.uuid4())[:8]
        order_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        final_order = {
            "order_id": order_id,
            "order_date": order_date,
            "items": self.order,
            "subtotal": subtotal,
            "tax": tax,
            "discount": discount,
            "total_amount": total,
            "order_type": "Pack Order" if order_type == "1" else "Table Booking"
        }

        billing = Bills(r"D:\Restaurant_management_system\src\Database\Bill.json")
        payment_success = billing.generate_invoice(final_order)

        if payment_success:
            self.append_to_file(self.order_file, final_order)
            print("Thank you for your order! Have a great day!")
            write_log(f"Order finalized successfully. Order ID: {order_id}")
            self.order.clear()
            self.save_orders()
        else:
            print("Payment failed or cancelled. Order not saved.")
            write_log(f"Payment failed for Order ID: {order_id}")

    def process(self):
        while True:
            print("\nOrder Your Food:")
            print("1. Add Item")
            print("2. Remove Item")
            print("3. Finalize Order")
            print("4. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_item()
            elif choice == "2":
                self.remove_item()
            elif choice == "3":
                self.finalize_order()
            elif choice == "4":
                print("Exiting Order Menu...")
                write_log("Exited order menu.")
                break
            else:
                print("Invalid choice. Try again.")
                write_log(f"Invalid menu choice: {choice}")
