import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

FILE = "expenses.json"

def load_data():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_expense():
    data = load_data()

    # date input
    while True:
        date = input("Enter date (YYYY-MM-DD) or press enter: ")
        if date == "":
            date = datetime.now().strftime("%Y-%m-%d")
            break
        elif len(date) == 10 and date[4] == "-" and date[7] == "-":
            break
        else:
            print("Invalid date format! Try again.")

    # category input
    while True:
        category = input("Enter category: ").strip()
        if category != "":
            break
        else:
            print("Category cannot be empty!")

    # amount input
    while True:
        try:
            amount = float(input("Enter amount: "))
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")
        except ValueError:
            print("Please enter a valid number.")

    desc = input("Enter description: ")

    expense = {
        "date": date,
        "category": category,
        "amount": amount,
        "description": desc
    }

    data.append(expense)
    save_data(data)

    print("Expense added successfully!")

def view_expenses():
    data = load_data()

    if not data:
        print("No data found.")
        return

    print("\n" + "-" * 40)
    print("        EXPENSE LIST        ")
    print("-" * 40)

    for e in data:
        print(f"{e['date']} | {e['category']} | ₹{e['amount']} | {e['description']}")

def monthly_summary():
    data = load_data()

    while True:
        month = input("Enter month (YYYY-MM): ")
        if len(month) == 7 and month[4] == "-":
            break
        else:
            print("Invalid format! Try again.")

    total = 0

    for e in data:
        if e["date"].startswith(month):
            total += e["amount"]

    if total == 0:
        print("No data for this month.")
    else:
        print(f"Total spending in {month}: ₹{total}")

def category_analysis():
    data = load_data()

    if not data:
        print("No data available.")
        return

    category_total = {}

    for e in data:
        cat = e["category"]
        if cat in category_total:
            category_total[cat] += e["amount"]
        else:
            category_total[cat] = e["amount"]

    print("\nCategory-wise spending:")
    for c in category_total:
        print(f"{c}: ₹{category_total[c]}")

    # highest category
    max_cat = max(category_total, key=category_total.get)
    print(f"\nHighest spending category: {max_cat}")

def show_chart():
    data = load_data()

    if not data:
        print("No data to show.")
        return

    category_total = {}

    for e in data:
        cat = e["category"]
        if cat in category_total:
            category_total[cat] += e["amount"]
        else:
            category_total[cat] = e["amount"]

    labels = []
    values = []

    for c in category_total:
        labels.append(c)
        values.append(category_total[c])

    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("Expense Distribution")
    plt.show()

def main():
    print("Welcome to Smart Expense Tracker")
    print("-" * 40)

    while True:
        print("\n1. Add Expense")
        print("2. View Expenses")
        print("3. Monthly Summary")
        print("4. Category Analysis")
        print("5. Show Pie Chart")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            monthly_summary()
        elif choice == "4":
            category_analysis()
        elif choice == "5":
            show_chart()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()
