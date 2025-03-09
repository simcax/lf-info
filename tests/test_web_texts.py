"""Tests for the web texts API"""

from unittest.mock import patch

import pytest

from lf_info.data.web_texts import WebTexts


def test_get_ticker_texts():
    """Test getting ticker texts"""
    web_texts = WebTexts()
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "AAPL, Apple Inc., Technology, Computers, 2021-06"
        ticker_texts = web_texts.get_ticker_texts_ticker()
        assert ticker_texts == ["AAPL, Apple Inc., Technology, Computers, 2021-06"]
        # ticker_texts = web_texts.get_ticker_texts_ticker()
    assert ticker_texts != "Failed to download file"


@pytest.fixture
def web_texts_data():
    web_texts_data = [
        "AAPL, Apple Inc., Technology, Computers, 2021-06",
        "MSFT, Microsoft Inc., Technology, Computers, 2021-06",
        "AMZN, Amazon Inc., Technology, Computers, 2021-06",
        "# This is a comment",
    ]
    return web_texts_data


def test_filter_out_comments(web_texts_data):
    """Tests the filter out comments function"""
    web_texts = WebTexts()
    filtered_texts = web_texts.filter_out_comments(web_texts_data)
    assert "# This is a comment" not in filtered_texts
