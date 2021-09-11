from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from math import ceil

class Rate:
    def __init__(self, start_time, end_time, value):
        self.start_time = start_time.time()
        self.end_time = end_time.time()
        self.value = value

    # Returns the start of the day of shift_date + 1 day
    def start_of_next_day(self, shift_date):
        return datetime.combine((shift_date + timedelta(days=1)).date(),
                                time(0, 0, 0))

    # Returns the number of minutes between time1 and time2
    # time2 is always larger than time1 except for the case
    # when time2 is 00:00:00
    def duration_in_min(self, time1, time2):
        datetime1 = datetime.combine(date.today(), time1)
        if (time2 == time(0, 0, 0)):
            datetime2 = self.start_of_next_day(datetime.today())
        else:
            datetime2 = datetime.combine(date.today(), time2)
        duration = datetime2 - datetime1
        duration_in_s = duration.total_seconds()
        
        return ceil(duration_in_s / 60)

    # Returns true if the shift_date is within the start
    # and end time of the rate, false otherwise
    def time_in_range(self, shift_datetime):
        if self.start_time <= self.end_time:
            return self.start_time <= shift_datetime.time() < self.end_time
        else:
            return (self.start_time <= shift_datetime.time()
                    or shift_datetime.time() < self.end_time)

    # Returns the total value if the robot works from shift_start_datetime
    # to rate end_time or shift_end_datetime, whichever is earlier.
    # Assumes that the shift_start_datetime passed in isi within the time range
    def calculate_value(self, shift_start_datetime, shift_end_datetime):
        lapsed_min = 0
        # Within the same day
        if (shift_start_datetime.time() <= self.end_time):
            new_end_time = min(
                shift_end_datetime,
                datetime.combine(shift_start_datetime.date(), self.end_time))
            lapsed_min = self.duration_in_min(shift_start_datetime.time(),
                                              new_end_time.time())
        # rate's start and end time spans across 2 day
        # so we just calculate the shift_start_datetime 
        # until the next day 00:00:00 as its possible
        # that the next day has a different rate
        else:
            new_end_time = min(shift_end_datetime,
                               self.start_of_next_day(shift_start_datetime))
            lapsed_min = self.duration_in_min(shift_start_datetime.time(),
                                              new_end_time.time())

        return self.value * lapsed_min, lapsed_min

    # Returns true if the other_rate and self are continuous, false otherwise
    def is_continuous(self, other_rate):
        return (self.start_time == other_rate.end_time
                and self.end_time == other_rate.start_time)

    def __str__(self):
        return f"start: {self.start_time}\nend: {self.end_time}\nvalue: {self.value}"
