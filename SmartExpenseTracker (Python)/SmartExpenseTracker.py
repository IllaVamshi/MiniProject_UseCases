import csv
import os
import matplotlib.pyplot as plt
from datetime import datetime

FILE_NAME = "expenses.csv"

# Add expense
def add_expense():
    date = input("Enter date (DD-MM-YYYY): ")
    try:
        datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        print("Invalid date format! Please use DD-MM-YYYY.\n")
        return

    category = input("Enter category : ").strip()
    if category == "":
        print("Category cannot be empty!\n")
        return

    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            print("Amount must be greater than 0.\n")
            return
    except ValueError:
        print("Invalid amount!\n")
        return

    description = input("Enter description: ")

    file_exists = os.path.exists(FILE_NAME)

    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["date", "category", "amount", "description"])

        writer.writerow([date, category, amount, description])

    print("Expense added successfully!\n")


# View all expenses
def view_expenses():
    if not os.path.exists(FILE_NAME):
        print("No data found.\n")
        return

    with open(FILE_NAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader, None)

        print("\n--- Expense List ---")
        for row in reader:
            print(row)


# Monthly Analysis
def monthly_analysis():
    if not os.path.exists(FILE_NAME):
        print("No data available.\n")
        return

    month = input("Enter month (MM-YYYY): ")
    total = 0

    with open(FILE_NAME, mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                row_date = datetime.strptime(row['date'], "%d-%m-%Y")
                if row_date.strftime("%m-%Y") == month:
                    total += float(row['amount'])
            except:
                continue

    print("\n--- Monthly Analysis ---")
    print(f"Month: {month}")
    print(f"Total Expense: ₹{total}\n")


# Category Analysis
def category_analysis():
    if not os.path.exists(FILE_NAME):
        print("No data available.\n")
        return {}

    categories = {}

    with open(FILE_NAME, mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                cat = row['category']
                amt = float(row['amount'])

                if cat in categories:
                    categories[cat] += amt
                else:
                    categories[cat] = amt
            except:
                continue

    print("\n--- Category Analysis ---")
    for cat, amt in categories.items():
        print(f"{cat}: ₹{amt}")

    return categories


# Highest spending category
def highest_category():
    categories = category_analysis()

    if categories:
        max_cat = max(categories, key=categories.get)
        print("\n--- Highest Spending Category ---")
        print(f"Category: {max_cat}\n")
    else:
        print("No data available\n")


# Pie chart
def show_pie_chart():
    categories = category_analysis()

    if categories:
        labels = list(categories.keys())
        values = list(categories.values())

        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title("Expense Distribution")
        plt.show()
    else:
        print("No data to display\n")


# Main menu
def main():
    while True:
        print("\n--- Smart Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Monthly Analysis")
        print("4. Category Analysis")
        print("5. Highest Spending Category")
        print("6. Show Pie Chart")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            monthly_analysis()
        elif choice == '4':
            category_analysis()
        elif choice == '5':
            highest_category()
        elif choice == '6':
            show_pie_chart()
        elif choice == '7':
            print("Exiting program...")
            break
        else:
            print("Invalid choice!\n")


if __name__ == "__main__":
    main()
