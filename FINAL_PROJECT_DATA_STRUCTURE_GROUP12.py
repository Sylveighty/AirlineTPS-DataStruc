"""
SkyPort TPS - Mini Transaction Processing System (Course-Level)
    Filename: FINAL_PROJECT_DATA_STRUCTURE_GROUP12.py
"""


def show_menu():
    # Simple menu display for CLI navigation.
    print("\n=== SkyPort TPS ===")
    print("[1] Insert Transaction (New Ticket/Check-in)")
    print("[2] Update Transaction")
    print("[3] Remove Transaction")
    print("[4] Search (Exact by ID)")
    print("[5] Search (Keyword)")
    print("[6] Display All Transactions (Sorted Ascending by ID)")
    print("[0] Exit")


def validate_non_empty_str(prompt):
    # Input validation loop keeps program stable (no empty strings).
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Error: input cannot be empty.")


def validate_float(prompt, min_value=0.0, allow_zero=True):
    # Parses numeric input; handles bad input without crashing.
    while True:
        try:
            value = float(input(prompt).strip())
            if allow_zero and value >= min_value:
                return value
            if not allow_zero and value > min_value:
                return value
            print("Error: value must be greater than {}.".format(min_value))
        except ValueError:
            print("Error: enter a valid number.")


def validate_choice(prompt, choices):
    # Ensures input matches one of the allowed options.
    choices_lower = [c.lower() for c in choices]
    while True:
        value = input(prompt).strip()
        if value.lower() in choices_lower:
            return choices[choices_lower.index(value.lower())]
        print("Error: choose from {}.".format(", ".join(choices)))


def validate_txn_id_format(txn_id):
    # Expected format: TXN-0001 (simple check, no regex needed).
    if not txn_id.startswith("TXN-"):
        return False
    digits = txn_id[4:]
    return digits.isdigit() and len(digits) == 4


def compute_baggage_fee(baggage_kg):
    # First 10kg free; excess charged per kg (O(1) computation).
    excess = max(0.0, baggage_kg - 10.0)
    return excess * 200.0


def compute_taxes(base_fare, baggage_fee):
    # Taxes based on subtotal (O(1) computation).
    return 0.12 * (base_fare + baggage_fee)


def compute_total(base_fare, baggage_fee, taxes):
    # Total is sum of components (O(1) computation).
    return base_fare + baggage_fee + taxes


def insert_transaction(transactions, index):
    # Insert uses dict index to block duplicate IDs (average O(1)).
    txn_id = validate_non_empty_str("Transaction ID (format TXN-0001): ")
    if not validate_txn_id_format(txn_id):
        print("Error: invalid transaction ID format.")
        return
    if txn_id in index:
        print("Error: transaction ID already exists.")
        return

    passenger_name = validate_non_empty_str("Passenger Name: ")
    flight_no = validate_non_empty_str("Flight No (e.g., PR123): ")
    destination = validate_non_empty_str("Destination: ")
    seat_class = validate_choice("Seat Class (Economy/Business/First): ",
                                ["Economy", "Business", "First"])
    base_fare = validate_float("Base Fare: ", min_value=0.0, allow_zero=False)
    baggage_kg = validate_float("Baggage (kg): ", min_value=0.0, allow_zero=True)

    baggage_fee = compute_baggage_fee(baggage_kg)
    taxes = compute_taxes(base_fare, baggage_fee)
    total_amount = compute_total(base_fare, baggage_fee, taxes)

    record = {
        "transaction_id": txn_id,
        "passenger_name": passenger_name,
        "flight_no": flight_no,
        "destination": destination,
        "seat_class": seat_class,
        "base_fare": base_fare,
        "baggage_kg": baggage_kg,
        "baggage_fee": baggage_fee,
        "taxes": taxes,
        "total_amount": total_amount,
    }
    transactions.append(record)
    index[txn_id] = len(transactions) - 1
    print("Transaction inserted successfully.")


def update_transaction(transactions, index):
    # Update uses index to find record quickly (average O(1)).
    txn_id = validate_non_empty_str("Enter Transaction ID to update: ")
    if txn_id not in index:
        print("Error: transaction not found.")
        return

    pos = index[txn_id]
    record = transactions[pos]

    passenger_name = validate_non_empty_str("Passenger Name: ")
    flight_no = validate_non_empty_str("Flight No (e.g., PR123): ")
    destination = validate_non_empty_str("Destination: ")
    seat_class = validate_choice("Seat Class (Economy/Business/First): ",
                                ["Economy", "Business", "First"])
    base_fare = validate_float("Base Fare: ", min_value=0.0, allow_zero=False)
    baggage_kg = validate_float("Baggage (kg): ", min_value=0.0, allow_zero=True)

    baggage_fee = compute_baggage_fee(baggage_kg)
    taxes = compute_taxes(base_fare, baggage_fee)
    total_amount = compute_total(base_fare, baggage_fee, taxes)

    record.update({
        "passenger_name": passenger_name,
        "flight_no": flight_no,
        "destination": destination,
        "seat_class": seat_class,
        "base_fare": base_fare,
        "baggage_kg": baggage_kg,
        "baggage_fee": baggage_fee,
        "taxes": taxes,
        "total_amount": total_amount,
    })
    print("Transaction updated successfully.")


def remove_transaction(transactions, index):
    # Remove updates index positions after pop (O(n) shift).
    txn_id = validate_non_empty_str("Enter Transaction ID to remove: ")
    if txn_id not in index:
        print("Error: transaction not found.")
        return

    pos = index[txn_id]
    transactions.pop(pos)
    del index[txn_id]

    # Update index positions after removal (O(n))
    for i in range(pos, len(transactions)):
        index[transactions[i]["transaction_id"]] = i

    print("Transaction removed successfully.")


def search_exact(transactions, index):
    # Exact search uses dict for average O(1) lookup.
    txn_id = validate_non_empty_str("Enter Transaction ID to search: ")
    if txn_id not in index:
        print("Error: transaction not found.")
        return
    record = transactions[index[txn_id]]
    print_record(record)


def search_keyword(transactions):
    # Keyword search scans list (O(n)).
    keyword = validate_non_empty_str("Enter keyword (name/destination/flight/seat class): ")
    keyword_lower = keyword.lower()

    # Linear search through list => O(n)
    matches = []
    for record in transactions:
        if (keyword_lower in record["passenger_name"].lower() or
                keyword_lower in record["destination"].lower() or
                keyword_lower in record["flight_no"].lower() or
                keyword_lower in record["seat_class"].lower()):
            matches.append(record)

    if not matches:
        print("No matches found.")
        return

    for record in matches:
        print_record(record)


def display_sorted(transactions):
    # Sorted display uses built-in sorted() per requirement.
    if not transactions:
        print("No transactions to display.")
        return

    # Built-in sorted uses Timsort; key lookup is O(1) average
    sorted_records = sorted(transactions, key=lambda r: r["transaction_id"])
    print_table_header()
    for record in sorted_records:
        print_table_row(record)


def print_record(record):
    # Print one record in key:value style.
    print("\n--- Transaction Record ---")
    for key, value in record.items():
        print(f"{key}: {value}")


def print_table_header():
    # Table header keeps output aligned for readability.
    header = (
        f"{'TXN ID':<10} | {'Passenger':<15} | {'Flight':<8} | {'Destination':<12} | "
        f"{'Class':<8} | {'Base':>8} | {'Bag(kg)':>7} | {'Bag Fee':>8} | "
        f"{'Taxes':>8} | {'Total':>8}"
    )
    print(header)
    print("-" * len(header))


def print_table_row(record):
    # Table row shows key numeric values with formatting.
    print(
        f"{record['transaction_id']:<10} | "
        f"{record['passenger_name']:<15} | "
        f"{record['flight_no']:<8} | "
        f"{record['destination']:<12} | "
        f"{record['seat_class']:<8} | "
        f"{record['base_fare']:>8.2f} | "
        f"{record['baggage_kg']:>7.1f} | "
        f"{record['baggage_fee']:>8.2f} | "
        f"{record['taxes']:>8.2f} | "
        f"{record['total_amount']:>8.2f}"
    )


def main():
    # Primary loop for menu-driven CLI.
    transactions = []
    index = {}  # transaction_id -> position (average O(1) lookup)

    while True:
        show_menu()
        choice = input("Select an option: ").strip()
        if choice == "1":
            insert_transaction(transactions, index)
        elif choice == "2":
            update_transaction(transactions, index)
        elif choice == "3":
            remove_transaction(transactions, index)
        elif choice == "4":
            search_exact(transactions, index)
        elif choice == "5":
            search_keyword(transactions)
        elif choice == "6":
            display_sorted(transactions)
        elif choice == "0":
            print("Exiting SkyPort TPS. Goodbye!")
            break
        else:
            print("Error: invalid option. Please try again.")


if __name__ == "__main__":
    main()


"""
REPORT NOTES
System Name: SkyPort TPS (Airport Ticketing/Check-in Transactions)
Description: A menu-driven, in-memory TPS that simulates airport ticketing/check-in
with basic data entry, updates, search, and sorted display. It focuses on simple
operations rather than advanced app features.

Data Structures Used + Justification:
- List of dictionaries for transactions: keeps records in one collection that is
  easy to loop over, display, and sort with built-in sorted(). This supports
  simple CRUD tasks clearly.
- Dictionary index (transaction_id -> list position): supports fast average O(1)
  exact search by ID so users can update/remove a specific transaction quickly.

Sample Transaction Scenario (Realistic Flow):
1) Staff checks in a passenger with ID TXN-0003 for flight PR456 to Cebu.
2) Base fare is 3200.00, baggage is 8.0 kg (no excess fee).
3) System computes taxes at 12% and totals the amount automatically.
4) Later, passenger adds extra baggage, so staff updates baggage to 14.0 kg and
   the system recomputes the excess fee, taxes, and new total.

Reflection (Challenges and Learnings):
- Challenge: Ensuring input is valid without crashing the program. The solution
  was to use loops and try/except for numbers.
- Challenge: Keeping the menu simple while still supporting all required features.
- Learning: A list is great for storing records, while a dictionary index makes
  exact search efficient. Combining them shows how different structures solve
  different needs in one program.
- Learning: Computing derived fields in one place (helper functions) prevents
  mistakes and keeps updates consistent.
"""
