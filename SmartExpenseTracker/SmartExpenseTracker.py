import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

file_name = "expenses.json"

# ---------- Load Data ----------
def get_data():
    if os.path.exists(file_name):
        try:
            f = open(file_name, "r")
            data = json.load(f)
            f.close()
            return data
        except:
            return []
    else:
        return []

# ---------- Save Data ----------
def save_data(data):
    f = open(file_name, "w")
    json.dump(data, f, indent=4)
    f.close()

# ---------- Add Expense ----------
def add_expense():
    data = get_data()

    date = input("Enter date (YYYY-MM-DD) or press enter: ")
    if date == "":
        date = datetime.now().strftime("%Y-%m-%d")

    category = input("Enter category: ")
    amount = input("Enter amount: ")
    desc = input("Enter description: ")

    try:
        amount = float(amount)
    except:
        print("Invalid amount!")
        return

    new_expense = {
        "date": date,
        "category": category,
        "amount": amount,
        "description": desc
    }

    data.append(new_expense)
    save_data(data)

    print("Expense added!")

# ---------- View Expenses ----------
def view_expenses():
    data = get_data()

    if len(data) == 0:
        print("No data found.")
        return

    print("\nExpenses List:")
    for i in range(len(data)):
        e = data[i]
        print(e["date"], "|", e["category"], "| ₹", e["amount"], "|", e["description"])

# ---------- Monthly Summary ----------
def monthly_summary():
    data = get_data()
    month = input("Enter month (YYYY-MM): ")

    total = 0
    days = []

    for e in data:
        if e["date"].startswith(month):
            total += e["amount"]
            if e["date"] not in days:
                days.append(e["date"])

    if len(days) == 0:
        print("No data for this month.")
        return

    avg = total / len(days)

    print("Total:", total)
    print("Average per day:", avg)

# ---------- Category Analysis ----------
def category_analysis():
    data = get_data()

    category_total = {}

    for e in data:
        cat = e["category"]
        if cat in category_total:
            category_total[cat] += e["amount"]
        else:
            category_total[cat] = e["amount"]

    if len(category_total) == 0:
        print("No data.")
        return

    print("\nCategory wise spending:")
    for c in category_total:
        print(c, ":", category_total[c])

    # find highest
    max_cat = None
    max_val = 0

    for c in category_total:
        if category_total[c] > max_val:
            max_val = category_total[c]
            max_cat = c

    print("Highest spending category:", max_cat)

    # simple suggestion
    total = sum(category_total.values())
    if max_val > total * 0.5:
        print("Try to reduce spending on", max_cat)

# ---------- Pie Chart ----------
def show_chart():
    data = get_data()

    category_total = {}

    for e in data:
        cat = e["category"]
        if cat in category_total:
            category_total[cat] += e["amount"]
        else:
            category_total[cat] = e["amount"]

    if len(category_total) == 0:
        print("No data to show.")
        return

    labels = []
    values = []

    for c in category_total:
        labels.append(c)
        values.append(category_total[c])

    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("Expenses")
    plt.show()

# ---------- Main Menu ----------
def main():
    while True:
        print("\n1. Add Expense")
        print("2. View Expenses")
        print("3. Monthly Summary")
        print("4. Category Analysis")
        print("5. Show Chart")
        print("6. Exit")

        ch = input("Enter choice: ")

        if ch == "1":
            add_expense()
        elif ch == "2":
            view_expenses()
        elif ch == "3":
            monthly_summary()
        elif ch == "4":
            category_analysis()
        elif ch == "5":
            show_chart()
        elif ch == "6":
            print("Exiting...")
            break
        else:
            print("Wrong choice")

# ---------- Run ----------
if __name__ == "__main__":
    main()
