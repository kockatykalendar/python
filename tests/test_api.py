import pytest

from kockatykalendar.api import get_available_datasets, get_events, Dataset


def test_datasets(requests_mock):
    requests_mock.get("https://data.kockatykalendar.sk/index.json", json=[
        {"start_year": 2020, "end_year": 2021, "school_year": "2020/2021", "filename": "2020_21.json"},
        {"start_year": 2019, "end_year": 2020, "school_year": "2019/2020", "filename": "2019_20.json"}
    ])

    ds = get_available_datasets()
    assert len(ds) == 2
    assert ds[0].start_year == 2020
    assert ds[1].start_year == 2019


def test_datasets_error(requests_mock):
    requests_mock.get("https://data.kockatykalendar.sk/index.json", status_code=500)
    with pytest.raises(ConnectionError):
        get_available_datasets()


def test_events(requests_mock):
    requests_mock.get("https://data.kockatykalendar.sk/2020_21.json", json=[
        {"name": "3. séria Riešky", "type": "seminar", "sciences": ["mat"], "date": {"start": "2020-04-26"},
         "contestants": {"min": "zs5", "max": "zs9"}, "places": ["online"], "organizers": ["riesky"],
         "link": "https://riesky.sk/"}
    ])

    events = get_events("2020_21.json")
    assert len(events) == 1
    assert events[0].name == "3. séria Riešky"

    events = get_events("https://data.kockatykalendar.sk/2020_21.json")
    assert len(events) == 1
    assert events[0].name == "3. séria Riešky"

    events = get_events(
        Dataset({"start_year": 2020, "end_year": 2021, "school_year": "2020/2021", "filename": "2020_21.json"})
    )
    assert len(events) == 1
    assert events[0].name == "3. séria Riešky"


def test_events_type():
    with pytest.raises(TypeError):
        get_events(123)


def test_events_404(requests_mock):
    requests_mock.get("https://data.kockatykalendar.sk/2020_21.json", status_code=404)
    assert get_events("2020_21.json") == []


def test_events_error(requests_mock):
    requests_mock.get("https://data.kockatykalendar.sk/2020_21.json", status_code=500)
    with pytest.raises(ConnectionError):
        get_events("2020_21.json")

