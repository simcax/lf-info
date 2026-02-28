# Test for the web page rendering the generalforsamling page

from flask import url_for


def test_generalforsamling_endpoint_loading(client):
    """
    Test the generalforsamling endpoint returns a 200 status code
    """
    response = client.get(url_for("main.generalforsamling"))
    assert response.status_code == 200
    assert b"Generalforsamling 2026" in response.data


def test_generalforsamling_has_version_number(client, monkeypatch):
    """
    Test that the generalforsamling page renders the VERSION env var
    """
    monkeypatch.setenv("VERSION", "1.2.3")
    response = client.get(url_for("main.generalforsamling"))
    assert b"Version 1.2.3" in response.data
