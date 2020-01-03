from display import *
import pytest

def test_get_current_and_future_temp():
    curr, future = get_current_and_future_temp()
    assert type(curr) == float
    assert type(future) == float

def test_format_temp():
    formatted = format_temp(4.51)
    assert formatted == "5°  "

def test_trains():
    trains = get_next_trains()
    assert len(trains) == 3
    print(trains)
