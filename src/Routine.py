"""
This module handles the procedural execution of requests over time,
implementing other modules.
Next steps for Routine.py:
    1. set up timed loop to run
    2. make api calls and get data
    3. link to email / sms for updates
    4. make this easily customizable
"""
from src import Stocks, Plots, Sector, Social
import time as t
from datetime import datetime as dt


class Routine:
    """
    API key and Stock obj are required to make a Routine

    Time properties use the time module and are in seconds
    For conversions, use datetime.fromtimestamp()
    """
    api_key = ""
    stocks = []
    frequency = 0
    start_time = 0
    running_time = 0
    duration = 0
    file_save_destination = ""
    notify_email = ""
    notify_sms = ""

    def __init__(self, api_key, stocks, frequency=60, duration=60, file_save_destination="", notify_email="",
                 notify_sms=""):
        self.api_key = api_key
        self.stocks = stocks
        self.frequency = frequency
        self.duration = duration
        self.file_save_destination = file_save_destination
        self.notify_email = notify_email
        self.notify_sms = notify_sms
        print(f"[SS]-[ROUTINE] New routine created: freq={self.frequency}, dur={self.duration}, stocks={self.stocks}")

    def setup(self, stocks=stocks, frequency=frequency, duration=duration, file_save_destination=file_save_destination,
              notify_email=notify_email, notify_sms=notify_sms):
        self.stocks = stocks
        self.frequency = frequency
        self.duration = duration
        self.file_save_destination = file_save_destination
        self.notify_email = notify_email
        self.notify_sms = notify_sms
        print(f"[SS]-[ROUTINE] Current routine changed: freq={self.frequency}, "
              f"dur={self.duration}, stocks={self.stocks}")

    def run(self, frequency=frequency, duration=duration):
        self.frequency = frequency
        self.duration = duration
        self.start_time = t.time()
        self.running_time = 0
        print(f"[SS]-[ROUTINE] Beginning routine at {dt.fromtimestamp(self.start_time)}")

        while self.running_time < self.duration:
            # Do stuff here
            self.get_last_workweek_data()

            # Delay
            self.running_time = t.time() - self.start_time
            t.sleep(self.frequency)

    def get_last_workweek_data(self):
        last_monday, last_friday = self.get_last_workweek()
        last_week_df = get_historical_data(self.batch_stocks, last_monday, last_friday,
                                           close_only=True, output_format="pandas", token=self.api_key)
        Plots.plot_stock(last_week_df, last_monday, last_friday, self.file_save_destination)

    @staticmethod
    def get_last_workweek():
        today = dt.today()
        last_monday = today + dt.timedelta(-today.weekday(), weeks=-1)
        last_friday = today + dt.timedelta(-today.weekday() - 3)

        return last_monday, last_friday
