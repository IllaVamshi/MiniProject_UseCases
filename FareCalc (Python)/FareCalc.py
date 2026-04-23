def calculate_fare(km, vehicle_type, hour):
    rates = {
        'economy': 10,
        'premium': 18,
        'suv': 25
    }

    base_rate = rates[vehicle_type]
    total_fare = km * base_rate

    surge_multiplier = 1.0

    if 17 <= hour <= 20:
        surge_multiplier = 1.5
        total_fare *= surge_multiplier

    return total_fare, surge_multiplier


def main():
    print("Welcome to CityCab Fare Estimator")
    print("-" * 40)

    while True:
        try:
            km = float(input("Enter distance (in km): "))
            if km > 0:
                break
            else:
                print("Distance must be greater than 0.")
        except ValueError:
            print("Please enter a valid number.")

    print("\nAvailable Vehicles: Economy, Premium, SUV")
    valid_types = ['economy', 'premium', 'suv']

    while True:
        vehicle_input = input("Enter vehicle type: ").strip().lower()

        if vehicle_input in valid_types:
            vehicle_type = vehicle_input
            break
        else:
            print("Invalid vehicle type! Try again.")

    while True:
        try:
            hour = int(input("Enter hour (0-23): "))
            if 0 <= hour <= 23:
                break
            else:
                print("Invalid hour! Try again.")
        except ValueError:
            print("Please enter a valid number.")

    fare, surge = calculate_fare(km, vehicle_type, hour)

    if vehicle_type == 'suv':
        display_vehicle = 'SUV'
    else:
        display_vehicle = vehicle_type.capitalize()

    # Receipt
    print("\n" + "=" * 30)
    print("        PRICE RECEIPT        ")
    print("=" * 30)

    print(f"Distance       : {km} km")
    print(f"Vehicle Type   : {display_vehicle}")
    print(f"Time           : {hour}:00")

    if surge > 1:
        print(f"Surge Pricing  : Active ({surge}x)")
    else:
        print("Surge Pricing  : Inactive")

    print("-" * 30)
    print(f"Total Fare     : ₹{fare:.2f}")
    print("=" * 30)


if __name__ == "__main__":
    main()
