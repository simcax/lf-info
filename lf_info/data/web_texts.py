"""Class for retrieving web texts from Google Drive"""

import csv
import io
import os

import requests
from loguru import logger


class WebTexts:
    def __init__(self):
        self.ticker_text_link_id = os.environ.get("WEB_TEXT_TICKER_LINK_ID")
        self.url = f"https://docs.google.com/spreadsheets/d/{self.ticker_text_link_id}/export?format=csv"

    def get_ticker_texts_ticker(self) -> list:
        response = requests.get(self.url)
        if response.status_code == 200:
            content = response.content.decode("utf-8")
            csv_file = io.StringIO(content)
            reader = csv.reader(csv_file)
            self.web_texts = self.filter_out_comments([row[0] for row in reader])

            logger.info("Retrieved new ticker texts")
        else:
            self.web_texts = ["Nyheder kan ikke vises på nuværende tidspunkt"]
            logger.error("Failed to download file")
        return self.web_texts

    def filter_out_comments(self, web_texts: list) -> list:
        return [text for text in web_texts if not text.startswith("#")]
