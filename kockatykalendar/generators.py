from typing import Iterable, List, Any

from kockatykalendar.events import Event


class CalendarGenerator:
    def items(self) -> Iterable:
        raise NotImplementedError()

    def event(self, item) -> Any[Event, List[Event]]:
        raise NotImplementedError()

    def generate(self) -> List[Event]:
        data = []
        for item in self.items():
            event = self.event(item)

            # Generator can return list of events
            if isinstance(event, list):
                for e in event:
                    if not isinstance(e, Event):
                        raise TypeError("Expected Event, got %s." % type(event))
                    data.append(e)
            # Or single event
            elif isinstance(event, Event):
                data.append(event)
            else:
                raise TypeError("Expected Event, got %s." % type(event))
        return data

    def to_json(self) -> List[dict]:
        data = []
        for item in self.generate():
            data.append(item.to_json())
        return data
