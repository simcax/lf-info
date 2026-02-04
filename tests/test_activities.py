# Tests getting activities from the foreninglet API
from datetime import datetime, timedelta
from unittest.mock import patch

from dotenv import load_dotenv

from lf_info.data.info import Info

load_dotenv()


def test_get_activities(activities):
    """Test getting activities from the foreninglet API"""

    # Patch the get_activities method to return the activities
    with patch("lf_info.data.info.Info.get_activities", return_value=activities):
        info = Info()
        activities = info.get_activities()
    assert len(activities) > 0


def test_get_classes(activities):
    """
    Test getting classes
    """
    # Patch the get_activities method to return the activities
    with patch("lf_info.data.info.Info.get_activities", return_value=activities):
        info = Info()
        classes = info.get_classes()
    assert len(classes) > 0


def test_get_classes_for_the_next_week(activities):
    """
    Test getting classes for the next week
    """
    # Alter the activities to have a start date in the next week and one not in the next week
    date_1 = datetime.now() + timedelta(days=1)
    date_2 = datetime.now() + timedelta(days=8)
    date_3 = datetime.now() + timedelta(days=15)

    activities[0]["ExternalDescriptions"][1]["Text"] = date_1.strftime(
        "%d. %b. %Y, kl. %H:%M"
    )
    activities[1]["ExternalDescriptions"][1]["Text"] = date_2.strftime(
        "%d. %b. %Y, kl. %H:%M"
    )
    activities[2]["ExternalDescriptions"][1]["Text"] = date_3.strftime(
        "%d. %b. %Y, kl. %H:%M"
    )

    # Patch the get_activities method to return the altered activities
    with patch("lf_info.data.info.Info.get_activities", return_value=activities):
        info = Info()
        classes = info.get_classes_for_the_next_week()
        assert len(classes) > 0
        for class_ in classes:
            assert isinstance(class_["StartDate"], datetime)
            assert class_["StartDate"] > datetime.now()
            assert class_["StartDate"] < info._next_week()
            assert class_["DepartmentId"] in ["6206", "7540"]


def test_update_activities_with_start_date(activities):
    """
    Test updating the activities with a start date
    """
    info = Info()
    classes = info.update_activities_with_start_date(activities)
    assert len(classes) > 0
    for class_ in classes:
        assert class_["StartDate"] == info._replace_weird_month_name_with_english(
            class_["ExternalDescriptions"][1]["Text"]
        )


def test_sort_classes_by_start_date(activities):
    """
    Test sorting classes by start date
    """
    info = Info()
    classes = info.update_activities_with_start_date(activities)
    sorted_classes = info.sort_classes_by_start_date(classes)
    assert len(sorted_classes) > 0
    for i in range(len(sorted_classes) - 1):
        assert sorted_classes[i]["StartDate"] <= sorted_classes[i + 1]["StartDate"]


def test_sort_classes_adds_missing_ledige_pladser_headline(activities):
    """
    Test that sort_classes_by_start_date adds missing "Ledige pladser" headline
    """
    info = Info()
    # Remove "Ledige pladser" headline from first activity
    activities[0]["ExternalDescriptions"] = [
        desc for desc in activities[0]["ExternalDescriptions"]
        if desc["Headline"] != "Ledige pladser"
    ]
    # Verify it's removed
    headlines_before = [
        desc["Headline"] for desc in activities[0]["ExternalDescriptions"]
    ]
    assert "Ledige pladser" not in headlines_before
    
    # Update with start date and sort
    classes = info.update_activities_with_start_date(activities)
    sorted_classes = info.sort_classes_by_start_date(classes)
    
    # Verify "Ledige pladser" was added
    headlines_after = [
        desc["Headline"] for desc in sorted_classes[0]["ExternalDescriptions"]
    ]
    assert "Ledige pladser" in headlines_after


def test_move_headlines_to_dict(activities):
    """
    Test moving headlines to dict
    """
    info = Info()
    classes = info.update_activities_with_start_date(activities)
    classes = info.move_headlines_to_dict(classes)
    assert len(classes) > 0
    for class_ in classes:
        assert isinstance(class_["Headlines"], dict)
        assert "Afviklingsdato" in class_["Headlines"]
        assert "Tilmelding åbner" in class_["Headlines"]
        assert "Sted" in class_["Headlines"]
        assert "Ledige pladser" in class_["Headlines"]
        assert "Instruktør" in class_["Headlines"]


def test_get_classes_list_for_web_page(activities):
    """
    Test getting a list of classes for the next week for the web page
    The list should be a list of activities where the startdate field is updated and sorted, and the headlines are moved to a dictionary
    """
    # Alter the activities to have a start date in the next week and one not in the next week
    date_1 = datetime.now() + timedelta(days=1)
    date_2 = datetime.now() + timedelta(days=8)
    date_3 = datetime.now() + timedelta(days=15)

    activities[0]["ExternalDescriptions"][1]["Text"] = date_1.strftime(
        "%d. %b. %Y, kl. %H:%M"
    )
    activities[1]["ExternalDescriptions"][1]["Text"] = date_2.strftime(
        "%d. %b. %Y, kl. %H:%M"
    )
    activities[2]["ExternalDescriptions"][1]["Text"] = date_3.strftime(
        "%d. %b. %Y, kl. %H:%M"
    )

    # Patch the get_activities method to return the activities
    with patch("lf_info.data.info.Info.get_activities", return_value=activities):
        info = Info()
        classes = info.get_classes_list_for_web_page()
        assert len(classes) > 0
        for class_ in classes:
            assert isinstance(class_["StartDate"], datetime)
            assert isinstance(class_["Headlines"], dict)
            assert "Afviklingsdato" in class_["Headlines"]
            assert "Tilmelding åbner" in class_["Headlines"]
            assert "Sted" in class_["Headlines"]
            assert "Ledige pladser" in class_["Headlines"]
            assert "Instruktør" in class_["Headlines"]
            assert class_["StartDate"] > datetime.now()
            assert class_["StartDate"] < info._next_week()


def test_sort_classes_adds_missing_ledige_pladser_headline(
    activities_without_ledige_pladser,
):
    """
    Test that sort_classes_by_start_date adds 'Ledige pladser' headline when missing.
    This verifies the fix for the page loading issue when activities don't contain
    a headline about the number of open spots.
    """
    info = Info()
    # First update activities with start date
    classes = info.update_activities_with_start_date(activities_without_ledige_pladser)
    
    # Verify the activity initially doesn't have "Ledige pladser"
    headlines_before = [
        ext_desc["Headline"] for ext_desc in classes[0]["ExternalDescriptions"]
    ]
    assert "Ledige pladser" not in headlines_before
    
    # Sort the classes (which should add the missing headline)
    sorted_classes = info.sort_classes_by_start_date(classes)
    
    # Verify the "Ledige pladser" headline was added
    headlines_after = [
        ext_desc["Headline"] for ext_desc in sorted_classes[0]["ExternalDescriptions"]
    ]
    assert "Ledige pladser" in headlines_after
    
    # Verify it was added with an empty text value
    ledige_pladser_entries = [
        ext_desc
        for ext_desc in sorted_classes[0]["ExternalDescriptions"]
        if ext_desc["Headline"] == "Ledige pladser"
    ]
    assert len(ledige_pladser_entries) == 1
    assert ledige_pladser_entries[0]["Text"] == ""
    
    # Verify other headlines are still present
    assert "Tilmelding åbner" in headlines_after
    assert "Afviklingsdato" in headlines_after
    assert "Sted" in headlines_after
    assert "Instruktør" in headlines_after
