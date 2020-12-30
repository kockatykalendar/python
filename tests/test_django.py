import json

from django.conf import settings

from kockatykalendar import scheme_version
from kockatykalendar.django import kockatykalendar_json
from test_generators import TestGenerator


def test_django_view():
    settings.configure()
    view = kockatykalendar_json(None, TestGenerator())
    data = json.loads(view.content)

    assert data["_kk_version"] == scheme_version
    assert len(data["data"]) == 3
    assert data["data"][0]["name"] == "KSP"
    assert data["data"][1]["name"] == "KMS"
    assert data["data"][2]["name"] == "FKS"
