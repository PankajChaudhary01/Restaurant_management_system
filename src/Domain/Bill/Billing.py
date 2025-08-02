import uuid
import json
from pathlib import Path
from datetime import datetime

LOG_FILE = r"D:\Restaurant_management_system\src\Logs\logs.txt"

def write_log(message):
    """Write logs to logs.txt with timestamp."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"[{datetime.now()}] {message}\n")

class Bills:
    PAYMENT_OPTIONS = {
        "1": "Cash",
        "2": "UPI",
        "3": "Credit Card",
        "4": "Debit Card",
    }
    DEFAULT_PAYMENT_METHOD = "Cash"
    LINE_SEPARATOR = "-" * 70

    def __init__(self, bill_path_str: str):
        self.bill_path = Path(bill_path_str)
        self.bill_path.parent.mkdir(parents=True, exist_ok=True)

    def choose_payment_method(self) -> tuple:
        try:
            print("\nChoose Payment Method:")
            for option_key, method_name in self.PAYMENT_OPTIONS.items():
                print(f"{option_key}. {method_name}")
            choice = input("Enter your choice: ").strip()
            payment_method = self.PAYMENT_OPTIONS.get(choice, self.DEFAULT_PAYMENT_METHOD)

            extra_info = {}
            if payment_method == "UPI":
                upi_id = input("Enter UPI ID: ").strip()
                extra_info = {"upi_id": upi_id}
            elif payment_method in ("Credit Card", "Debit Card"):
                card_name = input("Enter Cardholder Name: ").strip()
                card_number = input("Enter Card Number: ").strip()
                expiry_date = input("Enter Expiry Date (MM/YY): ").strip()
                cvv = input("Enter CVV: ").strip()
                extra_info = {
                    "card_name": card_name,
                    "card_number": card_number,
                    "expiry_date": expiry_date,
                    "cvv": cvv
                }

            write_log(f"Payment method chosen: {payment_method}")
            return payment_method, extra_info

        except Exception as e:
            print("Error while selecting payment method.")
            write_log(f"ERROR in choose_payment_method: {e}")
            return self.DEFAULT_PAYMENT_METHOD, {}

    def _generate_unique_id(self) -> str:
        return str(uuid.uuid4())[:8]

    def _display_invoice_details(self, invoice_id: str, order_details: dict):
        try:
            print("\n--- Invoice ---")
            print(f"Bill ID: {invoice_id}")
            print(f"Order ID: {order_details['order_id']}")
            print(f"Date: {order_details['order_date']}")
            print(self.LINE_SEPARATOR)
            print(f"{'Item Name':<20} {'Qty':<5} {'Unit Price (₹)':<15} {'Total (₹)':<10}")
            print(self.LINE_SEPARATOR)

            for item in order_details['items']:
                total_price = item['quantity'] * item['price']
                print(f"{item['name']:<20} {item['quantity']:<5} ₹{item['price']:<13.2f} ₹{total_price:<10.2f}")

            print(self.LINE_SEPARATOR)
            print(f"{'Subtotal':<50} ₹{order_details['subtotal']:.2f}")
            print(f"{'Tax (5%)':<50} ₹{order_details['tax']:.2f}")
            if order_details['discount'] > 0:
                print(f"{'Discount (10%)':<50} -₹{order_details['discount']:.2f}")
            print(f"{'Total Amount':<50} ₹{order_details['total_amount']:.2f}")
            print(self.LINE_SEPARATOR)

            write_log(f"Invoice displayed (ID: {invoice_id})")

        except Exception as e:
            print("Error while displaying invoice.")
            write_log(f"ERROR in _display_invoice_details: {e}")

    def generate_invoice(self, order_details: dict) -> bool:
        try:
            # Calculate bill amounts
            for item in order_details['items']:
                item['total_price'] = item['quantity'] * item['price']

            order_details['subtotal'] = sum(item['total_price'] for item in order_details['items'])
            order_details['tax'] = order_details['subtotal'] * 0.05
            order_details['discount'] = order_details['subtotal'] * 0.10 if order_details.get('apply_discount') else 0
            order_details['total_amount'] = order_details['subtotal'] + order_details['tax'] - order_details['discount']

            invoice_id = self._generate_unique_id()
            payment_method, extra_info = self.choose_payment_method()

            print(f"Selected Payment Method: {payment_method}")
            confirm_input = input("Confirm payment? (yes/no): ").strip().lower()
            if confirm_input not in ("yes", "y"):
                print("Payment cancelled.")
                write_log("Payment cancelled by user.")
                return False

            print("Payment successful")
            print("Thank you for dining with us!\n")
            write_log(f"Payment successful for Order ID: {order_details['order_id']}")

            # Display invoice
            self._display_invoice_details(invoice_id, order_details)

            # Save invoice
            invoice_data = {
                "invoice_id": invoice_id,
                "order_id": order_details['order_id'],
                "date": order_details['order_date'],
                "items": order_details['items'],
                "subtotal": order_details['subtotal'],
                "tax": order_details['tax'],
                "discount": order_details['discount'],
                "total_amount": order_details['total_amount'],
                "payment_method": payment_method,
                "payment_details": extra_info,
            }

            self._persist_invoice(invoice_data)
            write_log(f"Invoice generated and saved (ID: {invoice_id})")
            return True

        except Exception as e:
            print("Error while generating invoice.")
            write_log(f"ERROR in generate_invoice: {e}")
            return False

    def _load_existing_invoices(self) -> list:
        if not self.bill_path.is_file():
            return []
        try:
            with self.bill_path.open('r', encoding='utf-8') as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError) as e:
            write_log(f"ERROR loading invoices: {e}")
            return []

    def _persist_invoice(self, invoice_data: dict):
        try:
            all_invoices = self._load_existing_invoices()
            all_invoices.append(invoice_data)
            with self.bill_path.open('w', encoding='utf-8') as f:
                json.dump(all_invoices, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"FATAL: Could not save invoice to {self.bill_path}. Error: {e}")
            write_log(f"FATAL: Could not save invoice. Error: {e}")
