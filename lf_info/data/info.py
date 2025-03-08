# Class to retrieve activity data from ForeningLet API
from datetime import datetime, timedelta

import pandas as pd
from foreninglet_data.api import ForeningLet


class Info:
    def __init__(self) -> None:
        self.foreninglet = ForeningLet()

    def get_activities(self):
        return self.foreninglet.get_activities()

    def get_classes(self):
        activities = self.get_activities()
        classes = []
        # Get classes from activities by filtering all activities with DepartmentId = 6206
        departments = ["6206", "7540"]
        activity_types = ["6"]
        for activity in activities:
            if activity["Type"] in activity_types:
                classes.append(activity)
        return classes

    def _next_week(self):
        """
        Get the date for the next week
        """
        today = datetime.now()
        next_week = today + timedelta(days=7)
        return next_week

    # Function to parse date with both formats
    def parse_date(self, date_str):
        # Define the format for months with a period
        date_format_with_period = "%d. %b. %Y, kl %H:%M"

        # Define the format for months without a period
        date_format_without_period = "%d %b %Y, kl %H:%M"

        try:
            return datetime.strptime(date_str, date_format_with_period)
        except ValueError:
            return datetime.strptime(date_str, date_format_without_period)
        except TypeError:
            raise (TypeError(f"date_str is of type {type(date_str)} value {date_str}"))

    def get_classes_for_the_next_week(self):
        """
        Get classes for the next week
        """
        classes = self.get_classes()

        # Enrich the classes with a start date
        classes = self.update_activities_with_start_date(classes)

        next_week_classes = []
        for this_class in classes:
            start_date = this_class["StartDate"]
            start_date = (
                self.parse_date(start_date)
                if start_date != "Unknown"
                else datetime.strptime("01 jan 1970, kl 00:00", "%d %b %Y, kl %H:%M")
            )
            if start_date > datetime.now() and start_date < self._next_week():
                next_week_classes.append(this_class)
            this_class["StartDate"] = start_date

        return next_week_classes

    def _month_mapper(self, month):
        """
        Map a month to a number
        """
        month_dict = {
            "jan.": "jan",
            "jan": "jan",
            "feb.": "feb",
            "feb": "feb",
            "marts": "mar",
            "mar": "mar",
            "apr.": "apr",
            "apr": "apr",
            "april": "apr",
            "maj": "may",
            "juni": "jun",
            "jun": "jun",
            "juli": "jul",
            "jul": "jul",
            "aug.": "aug",
            "aug": "aug",
            "sept.": "sep",
            "sept": "sep",
            "sep": "sep",
            "okt.": "oct",
            "okt": "oct",
            "nov.": "nov",
            "nov": "nov",
            "dec.": "dec",
            "dec": "dec",
        }
        return month_dict[month.lower()]

    def _replace_weird_month_name_with_english(self, date_str):
        """
        Replace the month name with the English abbreviation
        """
        # Split the date string into a list of words
        try:
            date_str = date_str.replace(".", "")
            date_str = date_str.split()
            date_str[1] = self._month_mapper(date_str[1])
            date_str = " ".join(date_str)
        except IndexError:
            date_str = "Unknown"

        return date_str

    def _update_activity(self, activity):
        """
        Update an activity with a start date
        """
        # Convert the ExternalDescriptions to a DataFrame
        df = pd.json_normalize(activity["ExternalDescriptions"])

        # Find the row with Headline = "Afviklingsdato"
        start_date_row = df[df["Headline"] == "Afviklingsdato"]

        # Extract the Text value from the row
        # But only if there is a value
        if start_date_row.empty:
            start_date = "Unknown"
        else:
            start_date = start_date_row["Text"].values[0]

        # replace the month with the English abbreviation from the month_mapper
        start_date = self._replace_weird_month_name_with_english(start_date)

        # Add StartDate to the root level of the dictionary
        activity["StartDate"] = start_date

        return activity

    def update_activities_with_start_date(self, activities):
        """
        Update the activities with a start date
        """
        altered_activities = [
            self._update_activity(activity) for activity in activities
        ]
        return altered_activities

    def sort_classes_by_start_date(self, classes):
        """
        Sort classes by start date
        """

        sorted_classes = sorted(classes, key=lambda x: x["StartDate"])
        return sorted_classes

    def move_headlines_to_dict(self, classes):
        """
        Move headlines to dict
        """
        for class_ in classes:
            headlines = {}
            for ext_desc in class_["ExternalDescriptions"]:
                headlines[ext_desc["Headline"]] = ext_desc["Text"]
            class_["Headlines"] = headlines
        return classes

    def get_classes_list_for_web_page(self):
        """
        Get a list of classes for the next week for the web page
        """
        classes = self.get_classes_for_the_next_week()
        classes = self.sort_classes_by_start_date(classes)

        # Move headlines to a dictionary
        classes = self.move_headlines_to_dict(classes)

        return classes
