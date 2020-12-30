from datetime import date

import pytest

from kockatykalendar.events import Event, EventScience, EventType
from kockatykalendar.generators import CalendarGenerator


class TestGenerator(CalendarGenerator):
    def items(self):
        return ["KSP", "KMS", "FKS"]

    def event(self, item):
        return Event(
            name=item,
            sciences=[EventScience.MAT],
            type=EventType.SEMINAR,
            oragnizers=["trojsten"],
            places=["online"],
            date=Event.Dates(start=date(2020, 1, 1), end=date(2020, 1, 14))
        )


def test_generate():
    tg = TestGenerator()
    events = tg.generate()

    assert len(events) == 3
    assert events[0].name == "KSP"
    assert events[1].name == "KMS"
    assert events[2].name == "FKS"


def test_to_json():
    tg = TestGenerator()
    events = tg.to_json()

    assert len(events) == 3
    assert events[0]["name"] == "KSP"
    assert events[1]["name"] == "KMS"
    assert events[2]["name"] == "FKS"


def test_broken():
    class FriendlyGenerator(CalendarGenerator):
        def items(self):
            return ["KSP", "KMS", "FKS"]

        def event(self, item):
            return "hello"

    tg = FriendlyGenerator()
    with pytest.raises(TypeError):
        tg.generate()
