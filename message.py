import datetime

class AbstractCommand:
    def __str__(self):
        name = self.__class__.__name__
        return name + "()"


class AbstractSwitchCommand():
    def __init__(self, on):
        self.on = on

    def __str__(self):
        name = self.__class__.__name__
        return name + "(on=" + str(self.on) + ")"


class AbstractCommandConfirmationNotification:
    def __init__(self, was_successful):
        self.was_successful = was_successful

    def __str__(self):
        name = self.__class__.__name__
        return name + "(was_successful=" + str(self.was_successful) + ")"


class AuthorizeCommand():
    def __init__(self, pin):
        self.pin = pin

    def __str__(self):
        name = self.__class__.__name__
        return name + "(pin=" + str(self.pin) + ")"


class ChangePinCommand():
    def __init__(self, pin, new_pin):
        self.pin = pin
        self.new_pin = new_pin

    def __str__(self):
        name = self.__class__.__name__
        return name + "(pin=" + str(self.pin) + ", new_pin=" + str(self.new_pin) + ")"


class ResetPinCommand(AbstractCommand):
    pass


class PowerSwitchCommand(AbstractSwitchCommand):
    pass


class LEDSwitchCommand(AbstractSwitchCommand):
    pass


class SynchronizeDateAndTimeCommand():
    def __init__(self, year, month, day, hour, minute, second):
        d = datetime.datetime(year, month, day, hour, minute, second)

        self.year = d.year
        self.month = d.month
        self.day = d.day

        self.hour = d.hour
        self.minute = d.minute
        self.second = d.second

    def __str__(self):
        name = self.__class__.__name__
        return name + "(year=" + str(self.year) + ", month=" + str(self.month) + ", day=" + str(self.day) + ", hour=" + str(self.hour) + ", minute=" + str(self.minute) + ", second=" + str(self.second) + ")"


class RequestSettingsCommand(AbstractCommand):
    pass


class SetPowerLimitCommand():
    def __init__(self, power_limit_in_watt):
        self.power_limit_in_watt = power_limit_in_watt 

    def __str__(self):
        name = self.__class__.__name__
        return name + "(power_limit_in_watt=" + str(self.power_limit_in_watt) + ")"


class SetPricesCommand():
    def __init__(self, normal_price_in_cent, reduced_price_in_cent):
        self.normal_price_in_cent = normal_price_in_cent
        self.reduced_price_in_cent = reduced_price_in_cent

    def __str__(self):
        name = self.__class__.__name__
        return name + "(normal_price_in_cent=" + str(self.normal_price_in_cent) + ", reduced_price_in_cent=" + str(self.reduced_price_in_cent) + ")"


class SetReducedPeriodCommand():
    def __init__(self, is_active, start_time_in_minutes, end_time_in_minutes):
        self.is_active = is_active
        self.start_time_in_minutes = start_time_in_minutes
        self.end_time_in_minutes = end_time_in_minutes

    def __str__(self):
        name = self.__class__.__name__
        return name + "(is_active=" + str(self.is_active) + ", start_time_in_minutes=" + str(self.start_time_in_minutes) + ", end_time_in_minutes=" + str(self.end_time_in_minutes) + ")"


class RequestTimerStatusCommand(AbstractCommand):
    pass


class SetTimerCommand:
    def __init__(self, is_reset_timer, is_action_turn_on, target_second, target_minute, target_hour, target_day, target_month, target_year):
        self.is_reset_timer = is_reset_timer
        self.is_action_turn_on = is_action_turn_on
        self.target_second = target_second
        self.target_minute = target_minute
        self.target_hour = target_hour
        self.target_day = target_day
        self.target_month = target_month
        self.target_year = target_year

    def __str__(self):
        name = self.__class__.__name__
        return name + "(is_reset_timer=" + str(self.is_reset_timer) + ", is_action_turn_on=" + str(self.is_action_turn_on) + ", target_second=" + str(self.target_second) + ", target_minute=" + str(self.target_minute) + ", target_hour=" + str(self.target_hour) + ", target_day=" + str(self.target_day) + ", target_month=" + str(self.target_month) + ", target_year=" + str(self.target_year) + ")"


class RequestSchedulerCommand:
    def __init__(self, page_number):
        self.page_number = page_number

    def __str__(self):
        name = self.__class__.__name__
        return name + "(page_number=" + str(self.page_number) + ")"


class AuthorizationNotification(AbstractCommandConfirmationNotification):
    pass


class ChangePinNotification(AbstractCommandConfirmationNotification):
    pass


class ResetPinNotification(AbstractCommandConfirmationNotification):
    pass


class PowerSwitchNotification(AbstractCommandConfirmationNotification):
    pass


class LEDSwitchNotification(AbstractCommandConfirmationNotification):
    pass


class SynchronizeDateAndTimeNotification(AbstractCommandConfirmationNotification):
    pass


class RequestedSettingsNotification:
    def __init__(self, is_reduced_mode_active, normal_price_in_cent, reduced_price_in_cent, reduced_mode_start_time_in_minutes, reduced_mode_end_time_in_minutes, is_led_active, power_limit_in_watt):
        self.is_reduced_mode_active = is_reduced_mode_active
        self.normal_price_in_cent = normal_price_in_cent
        self.self = self.reduced_price_in_cent = reduced_price_in_cent
        self.reduced_mode_start_time_in_minutes = reduced_mode_start_time_in_minutes
        self.reduced_mode_end_time_in_minutes = reduced_mode_end_time_in_minutes
        self.is_led_active = is_led_active
        self.power_limit_in_watt = power_limit_in_watt

    def __str__(self):
        name = self.__class__.__name__
        return name + "(is_reduced_mode_active=" + str(self.is_reduced_mode_active) + ", normal_price_in_cent=" + str(self.normal_price_in_cent) + ", reduced_price_in_cent=" + str(self.reduced_price_in_cent) + ", reduced_mode_start_time_in_minutes=" + str(self.reduced_mode_start_time_in_minutes) + ", reduced_mode_end_time_in_minutes=" + str(self.reduced_mode_end_time_in_minutes) + ", is_led_active=" + str(self.is_led_active) + ", power_limit_in_watt=" + str(self.power_limit_in_watt) + ")"


class PowerLimitSetNotification(AbstractCommandConfirmationNotification):
    pass


class PricesSetNotification(AbstractCommandConfirmationNotification):
    pass


class ReducedPeriodSetNotification(AbstractCommandConfirmationNotification):
    pass


class RequestedTimerStatusNotification:
    def __init__(self, is_timer_running, is_action_turn_on, target_second, target_minute, target_hour, target_day, target_month, target_year, original_timer_length_in_seconds):
        self.is_timer_running = is_timer_running
        self.is_action_turn_on = is_action_turn_on
        self.target_second = target_second
        self.target_minute = target_minute
        self.target_hour = target_hour
        self.target_day = target_day
        self.target_month = target_month
        self.target_year = target_year
        self.original_timer_length_in_seconds = original_timer_length_in_seconds

    def __str__(self):
        name = self.__class__.__name__
        return name + "(is_action_turn_on=" + str(self.is_action_turn_on) + ", target_second=" + str(self.target_second) + ", target_minute=" + str(self.target_minute) + ", target_hour=" + str(self.target_hour) + ", target_day=" + str(self.target_day) + ", target_month=" + str(self.target_month) + ", target_year=" + str(self.target_year) + ", original_timer_length_in_seconds=" + str(self.original_timer_length_in_seconds) + ")"


class TimerSetNotification(AbstractCommandConfirmationNotification):
    pass


class Scheduler:
    def __init__(self, is_active, is_action_turn_on, repeat_on_weekdays, year, month, day, hour, minute):
        self.is_active = is_active
        self.is_action_turn_on = is_action_turn_on
        self.repeat_on_weekdays = repeat_on_weekdays
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute

    def __str__(self):
        name = self.__class__.__name__
        return name + "(is_active=" + str(self.is_active) + ", is_action_turn_on=" + str(self.is_action_turn_on) + ", repeat_on_weekdays=" + str(self.repeat_on_weekdays) + ", year=" + str(self.year) + ", month=" + str(self.month) + ", day=" + str(self.day) + ", hour=" + str(self.hour) + ", minute=" + str(self.minute) + ")"


class SchedulerRequestedNotification:
    def __init__(self, number_of_schedulers, schedulers):
        for scheduler in schedulers:
            assert isinstance(scheduler, Scheduler)

        self.number_of_schedulers = number_of_schedulers
        self.schedulers = schedulers

    def __str__(self):
        name = self.__class__.__name__
        schedulers = "["
        is_first = True
        for s in self.schedulers:
            if not is_first:
                schedulers += ", "

            schedulers += str(s)
            is_first = False
        schedulers += "]"

        return name + "(number_of_schedulers=" + str(self.number_of_schedulers) + ", schedulers=" + schedulers + ")"

