import pytest

from kockatykalendar.events import Event, EventContestant


def test_to_json():
    c = Event.Contestants().to_json()
    assert c["min"] is None
    assert c["max"] is None

    c = Event.Contestants(min="zs5", max="ss2").to_json()
    assert c["min"] == "zs5"
    assert c["max"] == "ss2"

    ec = EventContestant(EventContestant.SchoolType.ZAKLADNA, 5)
    ec2 = EventContestant(EventContestant.SchoolType.ZAKLADNA, 6)
    c = Event.Contestants(min=ec, max=ec2).to_json()
    assert c["min"] == "zs5"
    assert c["max"] == "zs6"


def test_from_json():
    c = Event.Contestants.from_json({
        "min": "zs5",
        "max": "zs6"
    })

    assert c.min == EventContestant(EventContestant.SchoolType.ZAKLADNA, 5)
    assert c.max == EventContestant(EventContestant.SchoolType.ZAKLADNA, 6)
    assert c.min != "zs5"


def test_validation():
    with pytest.raises(TypeError):
        c = Event.Contestants()
        c.min = "zs5"
        c.validate()

    with pytest.raises(TypeError):
        c = Event.Contestants()
        c.max = "zs5"
        c.validate()
