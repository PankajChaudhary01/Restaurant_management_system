# 🍽️ Restaurant Management System 

A beginner-friendly **Restaurant Management System** built in Python that handles authentication, menu management, order processing, billing, table booking, and staff operations. This project uses JSON files as a database to simulate real-world restaurant operations.

---

## 🚀 Features

### 🔑 Authentication
- Admin and Staff login system (hardcoded credentials for Admin).
- Staff sign-up and login functionalities.

### 🗂️ Menu Management (Admin)
- Add, update, and delete menu items.
- View all menu items stored in `Menu.json`.

### 🧾 Order Processing (Staff)
- Place new customer orders.
- Generate bills automatically.
- Track total orders and sales for the day.

### 💳 Billing
- Automatically calculate total amount including itemized details.
- Bills stored in `Bill.json` for future reference.

### 🍽️ Table Booking
- Book tables and manage reservations.
- View table configurations stored in `tables_config.json`.

### 👨‍🍳 Staff Operations
- Dedicated Staff Menu for order management.
- View daily sales and order summaries.

### 🗃️ Database (JSON-based)
- `Menu.json` → Menu items.
- `Order.json` → Customer orders.
- `Bill.json` → Billing details.
- `Table.json` → Table booking info.
- `Staff.json` → Staff user data.
- `admin.json` → Admin credentials.

---

## 🛠️ Technologies Used
- **Language:** Python 
- **Database:** JSON (file-based storage)
- **Paradigm:** OOP (Object-Oriented Programming)
- **Modules Used:**
  - `json` (data handling)
  - `os` (file operations)
  - `uuid` (unique IDs for orders/bills)
  - `datetime` (timestamps for logs)

---

## ▶️ How to Run

1. **Clone or Download this Repository**
   ```bash
   git clone https://github.com/PankajChaudhary01/Restaurant_management_system.git



