# Test for the web page rendering the activities

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
