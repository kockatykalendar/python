from datetime import date

import pytest

from kockatykalendar.events import Event, EventScience, EventType, EventContestant


def test_to_json():
    e = Event()
    e.name = "Testovací event"
    e.sciences = [EventScience.MAT, EventScience.FYZ]
    e.type = EventType.SEMINAR
    e.organizers = ["p-mat"]
    e.places = ["online"]
    e.date.start = date(2020, 1, 1)
    e.date.end = date(2020, 1, 2)
    e.contestants.min = EventContestant(raw="zs1")
    e.contestants.max = EventContestant(raw="zs9")
    json = e.to_json()

    assert json["name"] == e.name
    assert json["sciences"] == ["mat", "fyz"]
    assert json["type"] == "seminar"
    assert json["organizers"] == e.organizers
    assert json["places"] == e.places
    assert json["date"]["start"] == "2020-01-01"
    assert json["date"]["end"] == "2020-01-02"
    assert json["contestants"]["min"] == "zs1"
    assert json["contestants"]["max"] == "zs9"

    e.info = "Najlepšia udalosť široko blízko."
    e.color = "red"
    e.link = "https://kockatykalendar.sk"
    e.volatile = True
    e.cancelled = True
    json = e.to_json()

    assert json["info"] == e.info
    assert json["color"] == e.color
    assert json["link"] == e.link
    assert json["volatile"] == e.volatile
    assert json["cancelled"] == e.cancelled

    assert Event.from_json(json).to_json() == json


def test_to_json_custom_objects():
    e = Event(
        date=Event.Dates(start=date(2020, 1, 1), end=date(2020, 1, 2)),
        contestants=Event.Contestants(min="zs1", max="zs9")
    )
    e.name = "Testovací event"
    e.sciences = [EventScience.MAT, EventScience.FYZ]
    e.type = EventType.SEMINAR
    e.organizers = ["p-mat"]
    e.places = ["online"]
    json = e.to_json()

    assert json["date"]["start"] == "2020-01-01"
    assert json["date"]["end"] == "2020-01-02"
    assert json["contestants"]["min"] == "zs1"
    assert json["contestants"]["max"] == "zs9"


def test_validation():
    e = Event()
    with pytest.raises(ValueError):
        e.validate()    # Missing name

    e.name = 123
    with pytest.raises(TypeError):
        e.validate()    # Name must be string

    e.name = "Test"
    e.sciences = "mat"
    with pytest.raises(TypeError):
        e.validate()    # Sciences must be list

    e.sciences = []
    with pytest.raises(ValueError):
        e.validate()    # At least 1 science is required

    e.sciences = ["mat"]
    with pytest.raises(TypeError):
        e.validate()    # Sciences must be instance of EventScience

    e.sciences = [EventScience.MAT]
    with pytest.raises(ValueError):
        e.validate()    # Missing type

    e.type = "other"
    with pytest.raises(TypeError):
        e.validate()    # Type must be EventType

    e.type = EventType.OTHER
    e.places = "-1"
    with pytest.raises(TypeError):
        e.validate()    # Places must be a list

    e.places = []
    with pytest.raises(ValueError):
        e.validate()    # At least one place

    e.places = ["a", 2]
    with pytest.raises(TypeError):
        e.validate()    # All places must be strings

    e.places = ["a"]
    e.organizers = "trojsten"
    with pytest.raises(TypeError):
        e.validate()    # Organizers must be a list

    e.organizers = []
    with pytest.raises(ValueError):
        e.validate()    # At least 1 organizer

    e.organizers = ["trojsten", 3]
    with pytest.raises(TypeError):
        e.validate()    # All organizers must be strings

    e.organizers = ["trojsten"]
    e.date = []
    with pytest.raises(TypeError):
        e.validate()    # Dates must be Event.Dates

    e.date = Event.Dates(start=date(2020, 1, 1), end=date(2020, 1, 2))
    e.contestants = []
    with pytest.raises(TypeError):
        e.validate()    # Contestants must be Event.Contestants

    e.contestants = Event.Contestants()
    e.info = 12
    with pytest.raises(TypeError):
        e.validate()    # Info should be string

    e.info = "Yeah" * 100
    with pytest.raises(ValueError):
        e.validate()    # Info is too long

    e.info = "Yeah"
    e.color = 12
    with pytest.raises(TypeError):
        e.validate()    # Color should be a string

    e.color = "fijalova"
    with pytest.raises(ValueError):
        e.validate()    # Color format is invalid

    e.color = "#ffff"
    with pytest.raises(ValueError):
        e.validate()    # Color format is invalid

    e.color = "#fff"
    e.validate()

    e.link = 12
    with pytest.raises(TypeError):
        e.validate()    # Link should be a string

    e.link = "ftp://kockatykalendar.sk"
    with pytest.raises(ValueError):
        e.validate()    # Link should HTTP(s) URL

    e.link = "https://kockatykalendar.sk"
    e.volatile = -1
    with pytest.raises(TypeError):
        e.validate()    # Volatile should be bool

    e.volatile = True
    e.cancelled = -2
    with pytest.raises(TypeError):
        e.validate()    # Cancelled should be bool
