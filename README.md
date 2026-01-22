# SkyPort TPS (Mini Transaction Processing System)

This repository contains a simple, menu-driven, in-memory Transaction Processing System (TPS)
for an airport ticketing/check-in scenario. The goal is to demonstrate course-level data
structure usage using Python lists and dictionaries only.

## Requirements
- Python 3.x
- No external libraries

## How to Run
From the repository root:

```bash
python FINAL_PROJECT_DATA_STRUCTURE_GROUP12.py
```

## Features
- Insert, update, remove, and search transactions
- Keyword search across passenger name, destination, flight number, and seat class
- Sorted display by transaction ID using Python's built-in `sorted()`
- Input validation and computed fields (baggage fees, taxes, total amount)

## Data Structures Used
- **List of dictionaries** for storing transaction records (easy iteration/display/sort)
- **Dictionary index** for fast average O(1) lookup by transaction ID

## Notes
All data is stored in memory and is lost when the program exits.
