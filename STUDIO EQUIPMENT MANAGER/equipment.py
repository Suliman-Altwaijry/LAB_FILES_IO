from helpers import choose_equipment, confirm, borrowed_quantity, find_record, read_number, read_text, show_equipment
from storage import save_data


def add_equipment(data):
    name = read_text("Equipment name: ")
    category = read_text("Category: ")
    quantity = read_number("Total units owned (0 or more): ", minimum=0)
    equipment_id = data["next_equipment_id"]
    data["equipment"].append({"id": equipment_id, "name": name,
                              "category": category, "quantity": quantity})
    data["next_equipment_id"] += 1
    save_data(data)
    print(f"Equipment added. ID: {equipment_id}")


def view_equipment(data):
    show_equipment(data, data["equipment"])


def search_equipment(data):
    query = read_text("Search by name or category: ").casefold()
    matches = [equipment for equipment in data["equipment"]
               if query in equipment["name"].casefold()
               or query in equipment["category"].casefold()]
    show_equipment(data, matches)


def update_equipment(data):
    equipment = choose_equipment(data)
    print("Press Enter to keep the current value.")
    name = read_text(f"Name [{equipment['name']}]: ", default=equipment["name"])
    category = read_text(f"Category [{equipment['category']}]: ", default=equipment["category"])
    quantity = read_number(f"Total quantity [{equipment['quantity']}]: ",
                           minimum=0, default=equipment["quantity"])
    borrowed = borrowed_quantity(data, equipment["id"])
    if quantity < borrowed:
        raise ValueError(f"Cannot reduce total below {borrowed} borrowed unit(s).")
    equipment.update(name=name, category=category, quantity=quantity)
    save_data(data)
    print("Equipment updated.")


def delete_equipment(data):
    equipment = choose_equipment(data)
    if borrowed_quantity(data, equipment["id"]):
        raise ValueError("Cannot delete equipment while units are borrowed.")
    if not confirm(f"Delete {equipment['name']}? (yes/no): "):
        print("Deletion cancelled.")
        return
    data["equipment"].remove(equipment)
    save_data(data)
    print("Equipment deleted. Borrowing history has been kept.")
