"""Class for retrieving web texts from Google Drive"""

import csv
import io
import os

import requests
from loguru import logger
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


class WebTexts:
    def __init__(self):
        self.ticker_text_link_id = os.environ.get("WEB_TEXT_TICKER_LINK_ID")
        self.url = f"https://docs.google.com/spreadsheets/d/{self.ticker_text_link_id}/export?format=csv"

    def get_ticker_texts_ticker(self) -> list:
        try:
            retry = Retry(
                total=5,
                backoff_factor=2,
                status_forcelist=[429, 500, 502, 503, 504],
            )
            adapter = HTTPAdapter(max_retries=retry)
            session = requests.Session()
            session.mount("https://", adapter)
            response = session.get(self.url, timeout=180)
            if response.status_code == 200:
                content = response.content.decode("utf-8")
                csv_file = io.StringIO(content)
                reader = csv.reader(csv_file)
                self.web_texts = self.filter_out_comments([row[0] for row in reader])
                logger.info("Retrieved new ticker texts")
            else:
                self.web_texts = ["Nyheder kan ikke vises på nuværende tidspunkt"]
                logger.error("Failed to download file")
        except Exception as e:
            logger.exception(e)
            self.web_texts = ["Nyheder kan ikke vises på nuværende tidspunkt"]
            logger.error("Failed to download file")
        finally:
            return self.web_texts

    def filter_out_comments(self, web_texts: list) -> list:
        return [text for text in web_texts if not text.startswith("#")]
