# Test for the web page rendering the activities

import os
from unittest.mock import patch

from flask import url_for


def test_activity_endpoint_loading(client):
    """
    Test the activity endpoint
    """
    with patch("lf_info.data.info.Info.get_activities", return_value=[]):
        response = client.get(url_for("main.index"))
        assert response.status_code == 200
        assert b"Welcome to Lejre Fitness Info!" in response.data


def test_activity_list_loading(client, activities):
    """
    Test the activity list endpoint
    """
    with patch("lf_info.data.info.Info.get_activities", return_value=activities):
        response = client.get(url_for("main.activity_list"))
        assert response.status_code == 200
        assert b"Activity" in response.data
        assert b"Start Date" in response.data


def test_activities_reload_loading(client):
    """
    Test the activities reload endpoint
    """
    response = client.get(url_for("main.activities_reload"))
    assert response.status_code == 200


def test_activities_has_version_number(client):
    """
    Test that the activities page has the version number
    """
    os.environ["VERSION"] = "0.1"
    response = client.get(url_for("main.activity_list"))
    assert b"Version: 0.1" in response.data
