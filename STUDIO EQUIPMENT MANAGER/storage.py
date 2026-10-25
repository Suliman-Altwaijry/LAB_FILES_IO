import json
import os
import tempfile
from datetime import date
from pathlib import Path

from helpers import borrowed_quantity

DATA_FILE = Path(__file__).resolve().with_name("studio_data.json")


def save_data(data):
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=DATA_FILE.parent,
            prefix="studio_", suffix=".tmp", delete=False
        ) as file:
            temporary_path = Path(file.name)
            json.dump(data, file, indent=4, ensure_ascii=False)
            file.write("\n")
            file.flush()
            os.fsync(file.fileno())
        os.replace(temporary_path, DATA_FILE)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def validate_data(data):
    if not isinstance(data, dict) or any(
        not isinstance(data.get(key), list)
        for key in ("equipment", "transactions")
    ):
        raise ValueError("Data must contain equipment and transactions lists.")

    equipment_ids = set()
    transaction_ids = set()
    for collection, seen in (("equipment", equipment_ids),
                             ("transactions", transaction_ids)):
        for record in data[collection]:
            if not isinstance(record, dict):
                raise ValueError(f"Invalid record in {collection}.")
            record_id = record.get("id")
            if type(record_id) is not int or record_id < 1 or record_id in seen:
                raise ValueError(f"Invalid or duplicate ID in {collection}.")
            seen.add(record_id)
            minimum = 0 if collection == "equipment" else 1
            quantity = record.get("quantity")
            if type(quantity) is not int or quantity < minimum:
                raise ValueError(f"Invalid quantity in {collection}.")
            fields = ("name", "category") if collection == "equipment" else ("employee",)
            for field in fields:
                if not isinstance(record.get(field), str) or not record[field].strip():
                    raise ValueError(f"Missing or empty {field} in {collection}.")

    for transaction in data["transactions"]:
        equipment_id = transaction.get("equipment_id")
        if type(equipment_id) is not int or equipment_id < 1:
            raise ValueError("Invalid equipment ID in borrowing history.")
        if transaction.get("status") not in ("borrowed", "returned"):
            raise ValueError("Invalid transaction status.")
        for field in ("date", "return_date"):
            if field == "return_date" and field not in transaction:
                continue
            value = transaction.get(field)
            if not isinstance(value, str):
                raise ValueError("Invalid transaction date.")
            date.fromisoformat(value)
        if transaction["status"] == "borrowed" and equipment_id not in equipment_ids:
            raise ValueError("An active loan refers to missing equipment.")

    for equipment in data["equipment"]:
        if borrowed_quantity(data, equipment["id"]) > equipment["quantity"]:
            raise ValueError("Borrowed quantity exceeds the total quantity.")


    used_equipment_ids = equipment_ids | {
        transaction["equipment_id"] for transaction in data["transactions"]
    }
    for key, used_ids in (("next_equipment_id", used_equipment_ids),
                          ("next_transaction_id", transaction_ids)):
        next_id = data.get(key, max(used_ids, default=0) + 1)
        if type(next_id) is not int or next_id <= max(used_ids, default=0):
            raise ValueError(f"Invalid {key} counter.")
        data[key] = next_id


def load_data():
    if not DATA_FILE.exists():
        data = {"equipment": [], "transactions": [],
                "next_equipment_id": 1, "next_transaction_id": 1}
        save_data(data)
        return data
    with DATA_FILE.open(encoding="utf-8") as file:
        data = json.load(file)
    validate_data(data)
    return data
