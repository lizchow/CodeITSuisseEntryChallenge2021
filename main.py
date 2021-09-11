import json
import sys
from datetime import datetime

from rate import Rate
from robot import Robot


# Converts date in string format to datetime.
# Assume datetime without timezone
def shift_time_to_datetime(date_string):
    return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')


# Converts time in string format to datetime
def rate_time_to_datetime(time_string):
    return datetime.strptime(time_string, '%H:%M:%S')


# Returns a new Rate object with the start and end time and value
def parse_rates(rates_json):
    start_time = rate_time_to_datetime(rates_json['start'])
    end_time = rate_time_to_datetime(rates_json['end'])
    return Rate(start_time, end_time, rates_json['value'])


# Checks that the day and night rates are continuous and non-intersecting
# There should not be a period where the rates are undefined
def validate_rate_dates(day_rates, night_rates):
    if not day_rates.is_continuous(night_rates):
        raise RuntimeError("Invalid day and night rate dates")


if __name__ == "__main__":
    input_string = ''
    for line in sys.stdin:
        input_string += line

    input_json = json.loads(input_string)

    start = shift_time_to_datetime(input_json['shift']['start'])
    end = shift_time_to_datetime(input_json['shift']['end'])
    if start > end:
        raise RuntimeError(
            "Invalid start and end time. Start time cannot be later than end time"
        )

    robot_rates = input_json['roboRate']
    standard_day_rates = parse_rates(robot_rates['standardDay'])
    standard_night_rates = parse_rates(robot_rates['standardNight'])
    extra_day_rates = parse_rates(robot_rates['extraDay'])
    extra_night_rates = parse_rates(robot_rates['extraNight'])

    # Checks that all possible time periods are defined and non-intersecting
    validate_rate_dates(standard_day_rates, standard_night_rates)
    validate_rate_dates(standard_day_rates, extra_night_rates)
    validate_rate_dates(extra_day_rates, extra_night_rates)

    robot = Robot(standard_day_rates, standard_night_rates, extra_day_rates,
                  extra_night_rates)

    result = {"value": robot.get_total_value(start, end)}
    print(json.dumps(result))
