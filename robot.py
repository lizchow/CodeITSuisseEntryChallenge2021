from datetime import timedelta


class Robot:
    HOURS_PER_SHIFT = 8
    BREAK_HOUR = 1

    def __init__(self, standard_day, standard_night, extra_day, extra_night):
        self.std_day_rate = standard_day
        self.std_night_rate = standard_night
        self.extra_day_rate = extra_day
        self.extra_night_rate = extra_night

    # Returns true if the shift_date is a weekday, false otherwise
    def is_weekday(self, shift_date):
        return shift_date.weekday() < 5

    # Returns the chargeable rate for a given datetime
    def get_rate(self, shift_date):
        if self.is_weekday(shift_date) and self.std_day_rate.time_in_range(
                shift_date):
            return self.std_day_rate
        elif self.is_weekday(shift_date):
            return self.std_night_rate
        elif (not self.is_weekday(shift_date)
              and self.extra_day_rate.time_in_range(shift_date)):
            return self.extra_day_rate
        else:
            return self.extra_night_rate

    # Returns the total cost of the robot given that the robot is
    # continuously working from the start_time to the end_time
    def value_of_interval(self, start_time, end_time):
        temp_start_time = start_time
        total_value = 0
        while (temp_start_time < end_time):
            rate = self.get_rate(temp_start_time)
            value, lapsed_time = rate.calculate_value(temp_start_time,
                                                      end_time)
            # print(value, lapsed_time)
            total_value += value
            temp_start_time += timedelta(minutes=lapsed_time)

        return total_value

    # Returns the total cost of the robot when the robot works from
    # the start time to end time with breaks in between
    def get_total_value(self, start_time, end_time):
        temp_start_time = start_time
        total_value = 0
        while (temp_start_time < end_time):
            temp_end_time = min(
                end_time,
                temp_start_time + timedelta(hours=self.HOURS_PER_SHIFT))
            total_value += self.value_of_interval(temp_start_time,
                                                  temp_end_time)
            temp_start_time = temp_end_time + timedelta(hours=self.BREAK_HOUR)

        return total_value
