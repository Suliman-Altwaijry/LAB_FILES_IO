from datetime import date

from helpers import choose_equipment, borrowed_quantity, find_record, read_number, read_text
from storage import save_data


def borrow_equipment(data):
    equipment = choose_equipment(data)
    available = equipment["quantity"] - borrowed_quantity(data, equipment["id"])
    if available == 0:
        raise ValueError("All units are currently borrowed. Choose another item.")
    print(f"\nSelected: {equipment['name']} | Available: {available}")
    employee = read_text("Employee name: ")
    quantity = read_number("Quantity to borrow: ")
    available = equipment["quantity"] - borrowed_quantity(data, equipment["id"])
    if quantity > available:
        raise ValueError(f"Only {available} unit(s) available.")
    transaction_id = data["next_transaction_id"]
    data["transactions"].append({
        "id": transaction_id,
        "equipment_id": equipment["id"],
        "equipment_name": equipment["name"],
        "employee": employee,
        "quantity": quantity,
        "date": date.today().isoformat(),
        "status": "borrowed",
    })
    data["next_transaction_id"] += 1
    save_data(data)
    print(f"Borrowing saved. Transaction ID: {transaction_id}. Keep this ID for your return.")


def return_equipment(data):
    active = [loan for loan in data["transactions"] if loan["status"] == "borrowed"]
    if not active:
        print("No equipment is currently borrowed.")
        return
    print("\nActive loans:")
    for loan in active:
        name = loan.get("equipment_name", f"Equipment {loan['equipment_id']}")
        print(f"Transaction {loan['id']} | {loan['employee']} | {name} | Units: {loan['quantity']}")
    transaction = find_record(data["transactions"], read_number("Transaction ID: "))
    if transaction["status"] == "returned":
        raise ValueError("This transaction has already been returned.")
    transaction["status"] = "returned"
    transaction["return_date"] = date.today().isoformat()
    save_data(data)
    print("Equipment returned.")


def view_history(data):
    if not data["transactions"]:
        print("No borrowing history found.")
    for transaction in data["transactions"]:
        name = transaction.get("equipment_name", "Equipment")
        print(f"\nTransaction ID: {transaction['id']} | {transaction['employee']}")
        print(f"Equipment: {name} (ID: {transaction['equipment_id']}) | Quantity: {transaction['quantity']}")
        print(f"Borrowed: {transaction['date']} | Status: {transaction['status']}")
        if transaction.get("return_date"):
            print(f"Returned: {transaction['return_date']}")
