import os
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class StravaSegmentLeaderboardScraper:
    def __init__(self, segment_ids: list[str]):
        self.segment_ids = segment_ids
        self.results: dict[str, list] = {}

        # Configure and set up the driver:
        firefox_options = webdriver.FirefoxOptions()
        # firefox_options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=firefox_options)

    def _log_in_to_strava(self):
        self.driver.get("https://www.strava.com/login")
        email = self.driver.find_element(by=By.ID, value="email")
        email.clear()
        email.send_keys(os.environ["MY_STRAVA_EMAIL"])

        password = self.driver.find_element(by=By.ID, value="password")
        password.clear()
        password.send_keys(os.environ["MY_STRAVA_PASSWORD"])

        login_button = self.driver.find_element(by=By.ID, value="login-button")
        login_button.click()

    def _load_segment_page(self, segment_id):
        segment_url = f"https://www.strava.com/segments/{segment_id}"
        self.driver.get(segment_url)

    def _get_segment_name(self):
        return (
            self.driver.find_element(by=By.ID, value="js-full-name").text
            or "Failed to get segment name"
        )

    def _filter_leaderboard_to_today(self):
        buttons = self.driver.find_elements(by=By.CLASS_NAME, value="btn-unstyled")
        for button in buttons:
            if button.text == "All-Time":
                button.click()
                break

        options_parent = self.driver.find_element(by=By.CLASS_NAME, value="open-menu")
        options = options_parent.find_elements(by=By.TAG_NAME, value="li")
        today_option = options[1]
        today_option.click()

    def _get_all_results_from_leaderboard(self) -> list:
        results = []
        print(f"    Filtering leaderboard")
        self._filter_leaderboard_to_today()
        print(f"    Collecting all pages...")
        while True:
            time.sleep(3)  # there's probably a better way to do this
            leaderboard = self.driver.find_element(by=By.ID, value="results")
            html = leaderboard.get_attribute("innerHTML")
            leaderboard_data = pd.read_html(html)[0]
            results += leaderboard_data.values.tolist()

            # Either go to next page or break:
            try:
                time.sleep(3)  # there's probably a better way to do this
                next_button = self.driver.find_element(
                    by=By.CLASS_NAME, value="next_page"
                )
                css = next_button.get_attribute("class")
                if "disabled" in css:
                    break
                link = next_button.find_elements(by=By.TAG_NAME, value="a")[0]
                link.click()
            except Exception:
                print(f"Failed to go to next page!")
                break
        print("    Collected leaderboard!")
        return results

    def _close_driver(self):
        self.driver.quit()

    def run_scraper(self):
        print("Logging in to Strava...")
        self._log_in_to_strava()
        for segment_id in self.segment_ids:
            print(f"Loading segment {segment_id}")
            self._load_segment_page(segment_id)
            segment_name = self._get_segment_name()
            print(f"Loaded segment: {segment_name}. Collecting today's leaderboard...")
            self.results[segment_name] = self._get_all_results_from_leaderboard()
        print("Finished collecting all segments!")
        self._close_driver()

    def get_results(self):
        return self.results

    def _find_and_click_element(self, by=By.ID, value=""):
        try:
            element: WebElement = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((by, value))
            )
        except:
            self.driver.quit()
            print(f"Did not find {value} by {by}")
        element.click()
