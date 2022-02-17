import pytest
import sys

sys.path.append("../src")
from Theatre import Theatre
from seat_booker import make_booking_from_file


def test_single_booking():
    theatre = Theatre()
    response, seats = theatre.fulfill_request('r1', 2)

    assert response == True, "Unable to book in empty theatre"


def test_multiple_row_booking():
    theatre = Theatre()
    response, seats = theatre.fulfill_request('r1', 25)

    assert response == True, "Unable to book multiple rows in empty theatre"


def test_negative_booking():
    with pytest.raises(Exception):
        theatre = Theatre()
        response, seats = theatre.fulfill_request('r1', -1)


def test_zero_booking():
    with pytest.raises(Exception):
        theatre = Theatre()
        response, seats = theatre.fulfill_request('r1', 0)


def test_large_booking_through_file():
    base_path = "/Users/sjohar/Code/movie-seating-system/src/"
    infile = base_path + "input.txt"
    outfile = base_path + "output.txt"

    expected_output = ['R01 J1, J2, J3, J4, J5\n',
                       'R02 J9\n', 'R03 J13, J14\n',
                       'RO4 I1, I2, I3, I4, I5, I6, I7\n',
                       'R05 J18, J19, J20\n',
                       'R06 I11, I12, I13, I14\n',
                       'R07 I18, I19\n', 'RO8 H1, H2, H3, H4, H5\n',
                       'R09 H9, H10, H11, H12, H13, H14, H15, H16, H17, H18, H19, H20, G1, G2, G3, G4, G5, G6, G7, G8, G9\n']

    make_booking_from_file(infile, outfile)

    with open(outfile) as fp:
        lines = fp.readlines()
        assert lines == expected_output, "Incorrect Output"
