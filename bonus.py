import sys
from pathlib import Path

sys.dont_write_bytecode = True
BASE_DIR = Path(__file__).resolve().parent
for folder in (BASE_DIR / "STUDIO EQUIPMENT MANAGER", BASE_DIR / "bonus", BASE_DIR):
    if (folder / "storage.py").is_file():
        sys.path.insert(0, str(folder))
        break


from borrowing import borrow_equipment, return_equipment, view_history
from equipment import (
    add_equipment, delete_equipment, search_equipment, update_equipment, view_equipment,
)
from storage import DATA_FILE, load_data

MENU = """
=================================
    STUDIO EQUIPMENT MANAGER
=================================

1. Add Equipment
2. View All Equipment
3. Search Equipment
4. Update Equipment
5. Delete Equipment
6. Borrow Equipment
7. Return Equipment
8. View Borrowing History
9. Exit
"""


def main():
    try:
        data = load_data()
    except (OSError, ValueError) as error:
        print(f"Cannot load {DATA_FILE.name}: {error}")
        print("Existing data has not been overwritten.")
        return 1

    actions = {"1": add_equipment, "2": view_equipment,
               "3": search_equipment, "4": update_equipment,
               "5": delete_equipment, "6": borrow_equipment,
               "7": return_equipment, "8": view_history}
    labels = {"1": "Add Equipment", "2": "View All Equipment",
              "3": "Search Equipment", "4": "Update Equipment",
              "5": "Delete Equipment", "6": "Borrow Equipment",
              "7": "Return Equipment", "8": "Borrowing History"}
    while True:
        try:
            print(MENU)
            total = sum(item["quantity"] for item in data["equipment"])
            borrowed = sum(loan["quantity"] for loan in data["transactions"]
                           if loan["status"] == "borrowed")
            print(f"Equipment types: {len(data['equipment'])} | Units owned: {total}")
            print(f"Available: {total - borrowed} | Borrowed: {borrowed}")
            print("Type B during an action to go back. Updates: Enter keeps the current value.\n")
            choice = input("Select an option: ").strip()
            if choice == "9":
                print("All changes are saved. Goodbye👋")
                return 0
            if choice in actions:
                print(f"\n--- {labels[choice]} ---")
                actions[choice](data)
            else:
                print("Choose an option from 1 to 9.")
        except ValueError as error:
            print(f"{error}")
        except OSError as error:
            print(f"Could not save data: {error}")
            print("Stopping. Restart the program before trying again.")
            return 1
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
