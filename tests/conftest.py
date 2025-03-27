# pytest common fixtures
from datetime import datetime, timedelta

import pytest

from lf_info import create_app


@pytest.fixture
def activities():
    last_week = datetime.now() - timedelta(days=7)
    last_week_start_time = last_week - timedelta(hours=1)
    this_week = datetime.now()
    this_week_start_time = this_week - timedelta(hours=1)
    next_week = datetime.now() + timedelta(days=7)
    next_week_start_time = next_week - timedelta(hours=1)

    # Format the dates
    last_week_str = last_week.strftime("%d. %b. %Y, kl %H:%M")
    this_week_str = this_week.strftime("%d. %b. %Y, kl %H:%M")
    next_week_str = next_week.strftime("%d. %b. %Y, kl %H:%M")
    last_week_start_time_str = last_week_start_time.strftime("%d. %b. %Y, kl %H:%M")
    this_week_start_time_str = this_week_start_time.strftime("%d. %b. %Y, kl %H:%M")
    next_week_start_time_str = next_week_start_time.strftime("%d. %b. %Y, kl %H:%M")

    return [
        {
            "ActivityId": "152833",
            "Name": "Yoga",
            "PriceNow": 0,
            "OnlineEnrollmentEnabled": "1",
            "SettlementDate": "2024-11-13T19:00:00+0000",
            "EndDate": "0000-00-00T00:00:00+0000",
            "CloseDate": "0000-00-00T00:00:00+0000",
            "ExternalDescriptions": [
                {"Headline": "Tilmelding åbner", "Text": last_week_str},
                {"Headline": "Afviklingsdato", "Text": last_week_start_time_str},
                {"Headline": "Sted", "Text": "Multisalen"},
                {"Headline": "Ledige pladser", "Text": "2 ledige pladser (ud af 18)"},
                {"Headline": "Instruktør", "Text": "Jane Doe"},
            ],
            "Categories": [],
            "DepartmentId": "6206",
            "BackgroundColor": "#FFFFFF",
            "Type": "6",
        },
        {
            "ActivityId": "152834",
            "Name": "Advanced Yoga",
            "PriceNow": 100,
            "OnlineEnrollmentEnabled": "1",
            "SettlementDate": "2024-12-01T19:00:00+0000",
            "EndDate": "0000-00-00T00:00:00+0000",
            "CloseDate": "0000-00-00T00:00:00+0000",
            "ExternalDescriptions": [
                {"Headline": "Tilmelding åbner", "Text": this_week_str},
                {"Headline": "Afviklingsdato", "Text": this_week_start_time_str},
                {"Headline": "Sted", "Text": "Yoga Hall"},
                {"Headline": "Ledige pladser", "Text": "5 ledige pladser (ud af 20)"},
                {"Headline": "Instruktør", "Text": "John Doe"},
            ],
            "Categories": [],
            "DepartmentId": "6207",
            "BackgroundColor": "#FFFFFF",
            "Type": "6",
        },
        {
            "ActivityId": "152835",
            "Name": "Yoga for beginners",
            "PriceNow": 100,
            "OnlineEnrollmentEnabled": "1",
            "SettlementDate": "2024-12-01T19:00:00+0000",
            "EndDate": "0000-00-00T00:00:00+0000",
            "CloseDate": "0000-00-00T00:00:00+0000",
            "ExternalDescriptions": [
                {"Headline": "Tilmelding åbner", "Text": next_week_str},
                {"Headline": "Afviklingsdato", "Text": next_week_start_time_str},
                {"Headline": "Sted", "Text": "Yoga Hall"},
                {"Headline": "Ledige pladser", "Text": "5 ledige pladser (ud af 20)"},
                {"Headline": "Instruktør", "Text": "John Doe"},
            ],
            "Categories": [],
            "DepartmentId": "6207",
            "BackgroundColor": "#FFFFFF",
            "Type": "6",
        },
    ]


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            yield client
