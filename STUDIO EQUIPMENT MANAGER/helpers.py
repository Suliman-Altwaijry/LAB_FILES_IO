def read_text(prompt, default=None):
    while True:
        value = input(prompt).strip()
        if value.casefold() in ("b", "back"):
            raise ValueError("Action cancelled. Back to the main menu.")
        if not value and default is not None:
            return default
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def read_number(prompt, minimum=1, default=None):
    while True:
        value = input(prompt).strip()
        if value.casefold() in ("b", "back"):
            raise ValueError("Action cancelled. Back to the main menu.")
        if not value and default is not None:
            return default
        try:
            number = int(value)
            if number >= minimum:
                return number
        except ValueError:
            pass
        print(f"Enter a whole number of {minimum} or more.")


def find_record(records, record_id):
    for record in records:
        if record["id"] == record_id:
            return record
    raise ValueError(f"ID {record_id} was not found.")


def borrowed_quantity(data, equipment_id):
    return sum(
        transaction["quantity"] for transaction in data["transactions"]
        if transaction["equipment_id"] == equipment_id
        and transaction["status"] == "borrowed"
    )


def show_equipment(data, equipment_list):
    if not equipment_list:
        print("No equipment found.")
    for equipment in equipment_list:
        borrowed = borrowed_quantity(data, equipment["id"])
        available = equipment["quantity"] - borrowed
        print(f"\nID: {equipment['id']} | {equipment['name']} ({equipment['category']})")
        print(f"Total: {equipment['quantity']} | Borrowed: {borrowed} | Available: {available}")


def choose_equipment(data):
    if not data["equipment"]:
        raise ValueError("No equipment yet. Choose Add Equipment first.")
    show_equipment(data, data["equipment"])
    return find_record(data["equipment"], read_number("\nEnter the equipment ID: "))


def confirm(prompt):
    while True:
        answer = read_text(prompt).casefold()
        if answer in ("yes", "y"):
            return True
        if answer in ("no", "n"):
            return False
        print("Please enter yes or no.")
