import pytest
from bowling_alley import lane_cost, frame_score, lane_assignment


# lane_cost: day type branches
def test_known_day_types():
    assert lane_cost("weekday", 1, 2, 0, False) == 400
    assert lane_cost("weekend", 1, 2, 0, False) == 600


def test_unknown_day_type():
    with pytest.raises(ValueError, match="unknown day type"):
        lane_cost("holiday", 1, 2, 0, False)


# lane_cost: booking validation branches
@pytest.mark.parametrize(
    "games, players",
    [
        (0, 2),
        (1, 0),
        (1, 7),
    ],
)
def test_invalid_booking_conditions(games, players):
    with pytest.raises(ValueError, match="invalid booking"):
        lane_cost("weekday", games, players, 0, False)


def test_valid_booking_boundary():
    assert lane_cost("weekday", 1, 6, 0, False) == 500


# lane_cost: shoe rental branches
def test_valid_shoe_rentals():
    assert lane_cost("weekday", 1, 2, 1, False) == 450


def test_too_many_shoe_rentals():
    with pytest.raises(ValueError, match="too many shoe rentals"):
        lane_cost("weekday", 1, 2, 3, False)


# lane_cost: large group and membership branches
def test_large_group_surcharge():
    assert lane_cost("weekday", 1, 5, 0, False) == 500


def test_no_large_group_surcharge():
    assert lane_cost("weekday", 1, 4, 0, False) == 400


def test_league_member_discount():
    assert lane_cost("weekday", 1, 2, 0, True) == 320


def test_non_member_price():
    assert lane_cost("weekday", 1, 2, 0, False) == 400


# frame_score: invalid roll conditions
@pytest.mark.parametrize(
    "first, second",
    [
        (-1, 0),
        (11, 0),
        (5, -1),
    ],
)
def test_invalid_roll_conditions(first, second):
    with pytest.raises(ValueError, match="invalid roll"):
        frame_score(first, second, [])


# frame_score: strike, invalid frame, spare and open frame
def test_strike():
    assert frame_score(10, 0, [3, 4]) == 17


def test_invalid_frame():
    with pytest.raises(ValueError, match="invalid frame"):
        frame_score(7, 4, [])


def test_spare():
    assert frame_score(6, 4, [5]) == 15


def test_open_frame():
    assert frame_score(3, 4, []) == 7


# lane_assignment: all decision outcomes
def test_no_lanes_available():
    assert lane_assignment(4, False, 0) == "wait"


def test_kids_get_bumper_lane():
    assert lane_assignment(4, True, 1) == "bumper lane"


def test_large_group_gets_two_lanes():
    assert lane_assignment(8, False, 2) == "two lanes"


def test_large_group_waits_if_only_one_lane_free():
    assert lane_assignment(8, False, 1) == "wait"


def test_standard_group_gets_standard_lane():
    assert lane_assignment(4, False, 1) == "standard lane"
