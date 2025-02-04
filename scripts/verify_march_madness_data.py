#!/usr/bin/env python3
import csv
from collections import defaultdict

# Define the expected number of games per round for each year
EXPECTED_COUNTS = {
    "First Round": 32,
    "Second Round": 16,
    "Sweet 16": 8,
    "Elite Eight": 4,
    "Final Four": 2,
    "Championship": 1
}

def main():
    filename = "data//merged_dataset.csv"
    # Use a nested dictionary to count rounds per year.
    # For each year, counts[year][round_name] will hold the number of games in that round.
    counts = defaultdict(lambda: defaultdict(int))

    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            year = row["Year"]
            round_name = row["Round"]
            counts[year][round_name] += 1

    # Check each year's counts against the expected counts.
    ok = True
    # Sorting by year (converted to int)
    for year in sorted(counts.keys(), key=int):
        print(f"Year {year}:")
        for round_name, expected in EXPECTED_COUNTS.items():
            actual = counts[year].get(round_name, 0)
            if actual != expected:
                print(f"  {round_name}: expected {expected}, got {actual}")
                ok = False
            else:
                print(f"  {round_name}: OK")
    if ok:
        print("\nAll data is correct!")
    else:
        print("\nSome data is incorrect!")

if __name__ == "__main__":
    main() 