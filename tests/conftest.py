# pytest common fixtures
import pytest

from lf_info import create_app


@pytest.fixture
def activities():
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
                {"Headline": "Tilmelding åbner", "Text": "27. nov. 2024, kl. 08:00"},
                {"Headline": "Afviklingsdato", "Text": "4. dec. 2024, kl. 20:00"},
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
                {"Headline": "Tilmelding åbner", "Text": "1. dec. 2024, kl. 08:00"},
                {"Headline": "Afviklingsdato", "Text": "10. dec. 2024, kl. 20:00"},
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
                {"Headline": "Tilmelding åbner", "Text": "1. dec. 2024, kl. 08:00"},
                {"Headline": "Afviklingsdato", "Text": "10. dec. 2024, kl. 20:00"},
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
