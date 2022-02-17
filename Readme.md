# Movie Seat Reservation System

This command line tool enables the booking of theatre tickets. This is a part of the Walmart Interview process.

## Fulfillment Algorithm

- The fulfillment algorithm prioritizes the reservations in the order they appear.
- All seats in a reservation are tried to be assigned together on the same row.
- In the event that this cannot be done, the seats are split between multiple rows.
- Also, the algorithm begins allocating seats from the back of the theatre.
- For customer safety, a gap of three seats is maintained per customer group.

## Requirements:
- Python
- argparse `pip install argparse`

## Usage:

```seat_booker.py [-h] [--rows ROWS] [--columns COLUMNS] --infile INFILE --outfile OUTFILE```
