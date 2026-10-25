from pathlib import Path

file_path = Path(__file__).parent / "to_do.txt"

while True:
    choice = input("Add a new To-Do item? (y/n/exit): ").lower()

    if choice == "exit":
        print("Thank you for using the To-Do program, come back again soon")
        break

    elif choice == "y":
        item = input("Enter your To-Do item: ")

        with open(file_path, "a") as file:
            file.write(item + "\n")

        print("Item added!")

    elif choice == "n":
        choice = input("List your To-Do items? (y/n): ").lower()

        if choice == "y":
            try:
                with open(file_path, "r") as file:
                    print(file.read())
            except FileNotFoundError:
                print("No To-Do items found.")