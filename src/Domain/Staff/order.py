from src.Domain.Admin.AdminMenu import view_menu
import json
import os
import uuid
import datetime
from src.Domain.Bill.Billing import Bills
from src.Domain.Booking.Table import TableBooking
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
                return []
        return []

    def save_orders(self):
        """Save current orders to JSON."""
        with open(self.order_file, "w") as f:
            json.dump(self.order, f, indent=4)

    def append_to_file(self, filepath, data):
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as file:
                    existing = json.load(file)
            else:
                existing = []
        except json.JSONDecodeError:
            existing = []

        existing.append(data)
        with open(filepath, 'w') as file:
            json.dump(existing, file, indent=4)

    def add_item(self):
        view_menu()
        try:
            with open("src/Database/Menu.json", "r") as file:
                menu = json.load(file)  
        except FileNotFoundError:
            print("Menu file not found.")
            return
        except json.JSONDecodeError:
            print("Menu file is empty or broken.")
            return

        name = input("\nEnter item name to add: ").strip().lower()
        found = False

        for item in menu:
            if item["name"].lower() == name:
                try:
                    quantity = int(input(f"Enter quantity for {item['name']}: "))
                    if quantity <= 0:
                        print("Quantity must be at least 1.")
                        return
                except ValueError:
                    print("Invalid quantity. Please enter a number.")
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
                found = True
                break

        if not found:
            print("Item not found in the menu.")

    def remove_item(self):
        if not self.order:
            print("No items in your order to remove.")
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
            else:
                print("Invalid index.")
        except ValueError:
            print("Please enter a valid number.")

    def finalize_order(self):
        if not self.order:
            print("No items in order.")
            return

        print("\nSelect Order Type:")
        print("1. Pack Order")
        print("2. Table Booking")
        order_type = input("Enter choice (1 or 2): ").strip()

        if order_type == "2":
            # print("Booking table ....")
            tabBook=TableBooking()
            tabBook.book_table()
        elif order_type != "1":
            print("Invalid choice. Cancelling billing.")
            return

        print("\n--- Final Order ---")
        print(f"{'Name':<20} {'Qty':<4} {'Unit Price':<10} {'Total':<8}")
        print("-" * 60)
        for item in self.order:
            print(f"{item['name']:<20} {item['quantity']:<4} ₹{item['price']:<10} ₹{item['total_price']:<8}")

        subtotal = sum(item['total_price'] for item in self.order)
        tax_rate = 0.05
        discount_rate = 0.10 if subtotal >= 500 else 0

        tax = round(subtotal * tax_rate, 2)
        discount = round(subtotal * discount_rate, 2)
        total = round(subtotal + tax - discount, 2)

        print(f"\nSubtotal: ₹{subtotal}")
        print(f"Tax (5%): ₹{tax}")
        if discount_rate > 0:
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
            self.order.clear()
            self.save_orders()
        else:
            print("Payment failed or cancelled. Order not saved.")

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
                break
            else:
                print("Invalid choice. Try again.")
