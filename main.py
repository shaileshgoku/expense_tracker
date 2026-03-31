import os
import json
import datetime as dt

def load_data():
    if os.path.exists("data.json"):
        try:
            with open("data.json", "r") as file:
                if os.stat("data.json").st_size == 0:
                    return []
                return json.load(file)
        except json.JSONDecodeError:
            return []
    else:
        return []
    
expenses = load_data()

def save_data(expenses):
    with open("data.json", "w") as file:
        json.dump(expenses, file, indent=4)

def add_expense(expenses):
    try:
        amount = float(input("enter the amount: "))
    except ValueError:
        print("Invalid amount")
        return
    category = input("enter the category: ")
    description = input("enter the description: ")

    now = dt.datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")

    expense = {"amount": amount,"category":category,"description":description,"date": date }

    expenses.append(expense)

    save_data(expenses)

def view_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return

    for expense in expenses:
        print(
            f"Amount: {expense['amount']} | "
            f"Category: {expense['category']} | "
            f"Description: {expense['description']} | "
            f"Date: {expense['date']}"
        )

def show_total(expenses):
    if not expenses:
        print("No expenses to calculate.")
        return
    
    total = 0

    for expense in expenses:
        total += expense["amount"]
    
    print(f"Total Expense: {total}")

def show_categories(expenses):
    if not expenses:
        print("No categories available.")
        return

    categories = set()

    for expense in expenses:
        categories.add(expense["category"])

    print("Available Categories:")
    for category in categories:
        print(f"- {category}")

def show_category_summary(expenses):
    if not expenses:
        print("No expenses to summarize.")
        return

    summary = {}

    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]

        if category in summary:
            summary[category] += amount
        else:
            summary[category] = amount

    for category, total in summary.items():
        print(f"{category}: {total}")



def filter_by_category(expenses):
    if not expenses:
        print("No expenses available.")
        return

    category_input = input("Enter category to filter: ").lower()

    found = False

    for expense in expenses:
        if expense["category"].lower() == category_input:
            print(
                f"Amount: {expense['amount']} | "
                f"Category: {expense['category']} | "
                f"Description: {expense['description']} | "
                f"Date: {expense['date']}"
            )
            found = True

    if not found:
        print("No expenses found for this category.")

def main():
    expenses = load_data()

    while True:
        print("\n===== Expense Tracker =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Filter by Category")
        print("4. Show Total")
        print("5. Category Summary")
        print("6. show categories")
        print("7. Delete expenses")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            filter_by_category(expenses)

        elif choice == "4":
            show_total(expenses)

        elif choice == "5":
            show_category_summary(expenses)

        elif choice == "6":
            show_categories(expenses)

        elif choice == "7":
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()




