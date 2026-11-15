import pytest
from bowling_alley import lane_cost, frame_score, lane_assignment

#Example test cases:
def test_weekday_booking():
    assert lane_cost("weekday", 2, 4, 2, False) == 900

def test_open_frame():
    assert frame_score(3, 4, []) == 7

#Write the rest of the test cases so that the code is 90- 100% covered.
