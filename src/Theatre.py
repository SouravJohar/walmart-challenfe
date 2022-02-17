from Seat import Seat


class Theatre:

    def __init__(self, layout=(10, 20)):
        """
        Constructor to initialize a new Theatre.

        Parameters:
        ===========
            layout: tuple: A tuple representing the number of rows and columns in the theatre
        """

        if type(layout) not in [list, tuple]:
            raise Exception(
                "Expected type of `layout` to be list or tuple. Got {0}.".format(type(layout)))

        if type(layout[0]) is not int or type(layout[1]) is not int:
            raise Exception(
                "Expected type of `layout` to be tuple of ints. Got {0} and {0}.".format(type(layout[0]), type(layout[1])))

        if layout[0] <= 0 or layout[1] <= 0:
            raise Exception("Layout values should be greater than 0.")

        self.rows = layout[0]
        self.columns = layout[1]
        self.seats = self._build_layout()

    def _build_layout(self):
        """
        Internal method to build the seat layout representation of the theatre
        """

        seat_layout = []

        for i in range(self.rows):
            seat_row = []
            for j in range(self.columns):

                # The ID of a seat is alphabet-column
                id = chr(65 + i) + str(j + 1)
                seat = Seat(id)
                seat_row.append(seat)
            seat_layout.append(seat_row)

        return seat_layout

    def fulfill_request(self, reservation_id, num_seats):
        """
        Fulfills the request of a particular reservation.
        Note:
            The fulfillment algorithm prioritizes the reservations in the order they appear.
            All seats in a reservation are tried to be assigned together on the same row.
            In the event that this cannot be done, the seats are split between multiple rows.
            Also, the algorithm begins allocating seats from the back of the theatre.
            For customer safety, a gap of three seats is maintained per customer group.

        Parameters:
        ===========
            reservation_id: str: A string representing a reservation ID.
            num_seats: int: The number of seats to be booked

        Returns:
        ========
            is_fulfilled: bool: Was the request successfully fulfilled?
            seats_fulfilles: list[Seat] / None: A list of Seat objects representing the seats reserved 
        """

        if type(num_seats) not in [float, int]:
            raise Exception(
                "Expected type of `num_seats` to be int or float. Got {0}.".format(type(num_seats)))

        num_seats = int(num_seats)

        if num_seats <= 0:
            raise Exception("`num_seats` should be > 0.")

        is_fulfilled, seats_fulfilled = self._fulfill_request_in_single_row(
            reservation_id, num_seats)

        if is_fulfilled:
            return is_fulfilled, seats_fulfilled

        return self._fulfill_request_in_multiple_rows(reservation_id,
                                                      num_seats)

    def _fulfill_request_in_single_row(self, reservation_id, num_seats):
        """
        Internal method to fulfill a request in the same row if possible.
        """

        for i in range(self.rows - 1, -1, -1):

            seats_fulfilled = []

            for j in range(self.columns):

                if not self.seats[i][j].blocked and not self.seats[i][j].reserved:
                    seats_fulfilled.append(self.seats[i][j])

                elif len(seats_fulfilled) > 0 and (self.seats[i][j].blocked or self.seats[i][j].reserved):
                    seats_fulfilled = []

                if len(seats_fulfilled) == num_seats:
                    self._reserve_seats(seats_fulfilled, reservation_id)
                    self._block_nearby_seats(i, j, max_block=3)
                    return True, seats_fulfilled

        return False, []

    def _fulfill_request_in_multiple_rows(self, reservation_id, num_seats):
        """
        Internal method to fulfill a request in multiple rows if possible.
        """

        seats_fulfilled = []

        for i in range(self.rows - 1, -1, -1):
            seats_fulfilled_in_row = False
            last_seat_fulfilled_in_row = None

            for j in range(self.columns):

                if not self.seats[i][j].blocked and not self.seats[i][j].reserved:
                    seats_fulfilled.append(self.seats[i][j])
                    seats_fulfilled_in_row = True
                    last_seat_fulfilled_in_row = j

                if len(seats_fulfilled) == num_seats:
                    self._reserve_seats(seats_fulfilled, reservation_id)
                    self._block_nearby_seats(i, j, max_block=3)
                    return True, seats_fulfilled

            if seats_fulfilled_in_row:
                self._block_nearby_seats(
                    i, last_seat_fulfilled_in_row, max_block=3)

        return False, []

    def _reserve_seats(self, seats, reservation_id):
        """
        Mark the seats as "reserved" and assign the reservation_id to them once an allocation has been made.
        """

        for seat in seats:
            seat.reserved = True
            seat.reservation_id = reservation_id

    def _block_nearby_seats(self, row, column, max_block=3):
        """
        Once seat/s have been reserved, mark the next `max_block` seats as "blocked" for customer safety (covid)
        """

        for seat_column in range(len(self.seats[row])):
            if seat_column > column and seat_column <= column + max_block:
                self.seats[row][seat_column].blocked = True
