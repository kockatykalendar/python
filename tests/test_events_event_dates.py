from datetime import date

import pytest

from kockatykalendar.events import Event


def test_to_json():
    dates = Event.Dates(start=date(2020, 2, 1)).to_json()
    assert dates["start"] == "2020-02-01"
    assert dates["end"] is None
    assert dates["text"] is None

    dates = Event.Dates(start=date(2020, 2, 1), end=date(2020, 3, 2)).to_json()
    assert dates["start"] == "2020-02-01"
    assert dates["end"] == "2020-03-02"
    assert dates["text"] is None

    dates = Event.Dates(start=date(2020, 2, 1), text="hello").to_json()
    assert dates["start"] == "2020-02-01"
    assert dates["end"] is None
    assert dates["text"] == "hello"


def test_from_json():
    dates = Event.Dates.from_json({
        "start": "2020-01-02"
    })
    assert dates.start == date(2020, 1, 2)
    assert dates.end is None
    assert dates.text is None

    dates = Event.Dates.from_json({
        "start": "2020-01-02",
        "end": "2020-02-02",
        "text": "november"
    })
    assert dates.start == date(2020, 1, 2)
    assert dates.end == date(2020, 2, 2)
    assert dates.text == "november"


def test_validation():
    with pytest.raises(ValueError):
        Event.Dates().validate()

    with pytest.raises(TypeError):
        Event.Dates(start="2020-02-01").validate()

    with pytest.raises(TypeError):
        Event.Dates(start=date(2020, 1, 1), end="2020-02-01").validate()
