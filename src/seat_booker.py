from Theatre import Theatre
import argparse


def make_booking_from_file(input_file_path, output_file_path, layout=(10, 20)):
    """
    Helper method that calls the Theatre object's fulfill method to make reservations.
    """

    theatre = Theatre(layout)
    processed_requests = []

    with open(input_file_path) as fp:
        for line in fp.readlines():
            reservation_id, num_seats = line.split()

            num_seats = int(num_seats)

            is_fulfilled, seats = theatre.fulfill_request(
                reservation_id, num_seats)

            if is_fulfilled:
                processed_requests.append(
                    [reservation_id, [seat.id for seat in seats]])
            else:
                processed_requests.append(
                    [reservation_id, ["UNABLE TO MAKE RESERVATION"]])

    with open(output_file_path, 'w') as fp:

        for reservation_id, seats in processed_requests:
            fp.write(reservation_id + " " + ", ".join(seats) + "\n")

    return output_file_path


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--rows', type=int, required=False,
                        help="Number of rows in the theatre. Default = 10.", default=10)
    parser.add_argument('--columns', type=int, required=False,
                        help="Number of columns in the theatre. Default = 20.", default=20)
    parser.add_argument('--infile', type=str, required=True)
    parser.add_argument('--outfile', type=str, required=True)

    args = parser.parse_args()

    outfile = make_booking_from_file(args.infile, args.outfile,
                                     layout=(args.rows, args.columns))
    print("Reservations made. Output file: {0}".format(outfile))
