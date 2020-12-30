import pytest

from kockatykalendar.events import EventContestant


def test_to_raw():
    c = EventContestant()
    assert c.raw is None

    c = EventContestant(EventContestant.SchoolType.STREDNA, 4)
    assert c.raw == "ss4"

    c = EventContestant(EventContestant.SchoolType.ZAKLADNA, 8)
    assert c.raw == "zs8"


def test_from_raw():
    c = EventContestant(raw="ss4")
    assert c.type == EventContestant.SchoolType.STREDNA
    assert c.year == 4

    c = EventContestant(raw=None)
    assert c.type == None
    assert c.year == None


def test_invalid():
    # Year is required with type.
    with pytest.raises(ValueError):
        c = EventContestant(type=EventContestant.SchoolType.STREDNA)
        c.validate()

    # Year must be int.
    with pytest.raises(TypeError):
        c = EventContestant(type=EventContestant.SchoolType.STREDNA, year="2")
        c.validate()

    # Year must be in range 1-4 for SS.
    with pytest.raises(ValueError):
        c = EventContestant(type=EventContestant.SchoolType.STREDNA, year=5)
        c.validate()

    # Year must be in range 1-9 for ZS.
    with pytest.raises(ValueError):
        c = EventContestant(type=EventContestant.SchoolType.ZAKLADNA, year=-1)
        c.validate()

    # School type must be EventContestant.SchoolType
    with pytest.raises(TypeError):
        c = EventContestant(type="zs", year=1)
        c.validate()
