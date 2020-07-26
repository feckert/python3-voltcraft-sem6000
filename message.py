import datetime
import enum

def _list_values_to_enum(enum_class, list_of_values):
    list_of_enums = []
    for v in list_of_values:
        list_of_enums.append(enum_class(v))
    return list_of_enums

def _format_list_of_objects(format_object_lambda, list_of_objects):
    is_first = True
    formatted_string = "["
    for o in list_of_objects:
        if not is_first:
            formatted_string += ", "
        formatted_string += format_object_lambda(o)
        is_first = False
    formatted_string += "]"

    return formatted_string


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
    def __init__(self, normal_price_in_cent, reduced_period_price_in_cent):
        self.normal_price_in_cent = normal_price_in_cent
        self.reduced_period_price_in_cent = reduced_period_price_in_cent

    def __str__(self):
        name = self.__class__.__name__
        return name + "(normal_price_in_cent=" + str(self.normal_price_in_cent) + ", reduced_period_price_in_cent=" + str(self.reduced_period_price_in_cent) + ")"


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


class AddSchedulerCommand:
    def __init__(self, scheduler):
        assert isinstance(scheduler, Scheduler)

        self.scheduler = scheduler

    def __str__(self):
        name = self.__class__.__name__
        return name + "(scheduler=" + str(self.scheduler) + ")"


class EditSchedulerCommand:
    def __init__(self, slot_id, scheduler):
        assert isinstance(scheduler, Scheduler)

        self.slot_id = slot_id
        self.scheduler = scheduler

    def __str__(self):
        name = self.__class__.__name__
        return name + "(slot_id=" + str(self.slot_id) + ", scheduler=" + str(self.scheduler) + ")"


class RemoveSchedulerCommand:
    def __init__(self, slot_id):
        self.slot_id = slot_id

    def __str__(self):
        name = self.__class__.__name__
        return name + "(slot_id=" + str(self.slot_id) + ")"


class RequestRandomModeStatusCommand(AbstractCommand):
    pass 


class SetRandomModeCommand:
    def __init__(self, is_active, active_on_weekdays, start_hour, start_minute, end_hour, end_minute):
        active_on_weekdays = _list_values_to_enum(Weekday, active_on_weekdays)

        self.is_active = is_active
        self.active_on_weekdays = active_on_weekdays
        self.start_hour = start_hour
        self.start_minute = start_minute
        self.end_hour = end_hour
        self.end_minute = end_minute

    def __str__(self):
        weekday_formatter = lambda w: w.name
        active_on_weekdays = _format_list_of_objects(weekday_formatter, self.active_on_weekdays)

        name = self.__class__.__name__
        return name + "(is_active=" + str(self.is_active) + ", active_on_weekdays=" + active_on_weekdays + ", start_hour=" + str(self.start_hour) + ", start_minute=" + str(self.start_minute) + ", end_hour=" + str(self.end_hour) + ", end_minute=" + str(self.end_minute) + ")"


class SetDeviceNameCommand:
        def __init__(self, new_name):
            self.new_name = new_name

        def __str__(self):
            command = self.__class__.__name__
            return command + "(new_name=" + str(self.new_name) + ")"


class RequestDeviceSerialCommand(AbstractCommand):
    pass


class RequestMeasurementCommand(AbstractCommand):
    pass


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
    def __init__(self, is_reduced_period, normal_price_in_cent, reduced_period_price_in_cent, reduced_period_start_time_in_minutes, reduced_period_end_time_in_minutes, is_led_active, power_limit_in_watt):
        self.is_reduced_period = is_reduced_period
        self.normal_price_in_cent = normal_price_in_cent
        self.reduced_period_price_in_cent = reduced_period_price_in_cent
        self.reduced_period_start_time_in_minutes = reduced_period_start_time_in_minutes
        self.reduced_period_end_time_in_minutes = reduced_period_end_time_in_minutes
        self.is_led_active = is_led_active
        self.power_limit_in_watt = power_limit_in_watt

    def __str__(self):
        name = self.__class__.__name__
        return name + "(is_reduced_period=" + str(self.is_reduced_period) + ", normal_price_in_cent=" + str(self.normal_price_in_cent) + ", reduced_periiod_price_in_cent=" + str(self.reduced_period_price_in_cent) + ", reduced_period_start_time_in_minutes=" + str(self.reduced_period_start_time_in_minutes) + ", reduced_period_end_time_in_minutes=" + str(self.reduced_period_end_time_in_minutes) + ", is_led_active=" + str(self.is_led_active) + ", power_limit_in_watt=" + str(self.power_limit_in_watt) + ")"


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


class Weekday(enum.Enum):
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6


class Scheduler:
    def __init__(self, is_active, is_action_turn_on, repeat_on_weekdays, year, month, day, hour, minute):
        repeat_on_weekdays = _list_values_to_enum(Weekday, repeat_on_weekdays)

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

        weekday_formatter = lambda w: w.name
        repeat_on_weekdays = _format_list_of_objects(weekday_formatter, self.repeat_on_weekdays)

        return name + "(is_active=" + str(self.is_active) + ", is_action_turn_on=" + str(self.is_action_turn_on) + ", repeat_on_weekdays=" + repeat_on_weekdays + ", year=" + str(self.year) + ", month=" + str(self.month) + ", day=" + str(self.day) + ", hour=" + str(self.hour) + ", minute=" + str(self.minute) + ")"


class SchedulerEntry:
    def __init__(self, slot_id, scheduler):
        assert isinstance(scheduler, Scheduler)

        self.slot_id = slot_id
        self.scheduler = scheduler

    def __str__(self):
        name = self.__class__.__name__
        return name + "(slot_id=" + str(self.slot_id) + ", scheduler=" + str(self.scheduler) + ")"


class SchedulerRequestedNotification:
    def __init__(self, number_of_schedulers, scheduler_entries):
        for scheduler_entry in scheduler_entries:
            assert isinstance(scheduler_entry, SchedulerEntry)

        self.number_of_schedulers = number_of_schedulers
        self.scheduler_entries = scheduler_entries

    def __str__(self):
        name = self.__class__.__name__

        scheduler_entries = _format_list_of_objects(str, self.scheduler_entries)

        return name + "(number_of_schedulers=" + str(self.number_of_schedulers) + ", scheduler_entries=" + scheduler_entries + ")"


class SchedulerSetNotification(AbstractCommandConfirmationNotification):
    pass


class RandomModeStatusRequestedNotification:
    def __init__(self, is_active, active_on_weekdays, start_hour, start_minute, end_hour, end_minute):
        active_on_weekdays = _list_values_to_enum(Weekday, active_on_weekdays)

        self.is_active = is_active
        self.active_on_weekdays = active_on_weekdays
        self.start_hour = start_hour
        self.start_minute = start_minute
        self.end_hour = end_hour
        self.end_minute = end_minute

    def __str__(self):
        weekday_formatter = lambda w: w.name
        active_on_weekdays = _format_list_of_objects(weekday_formatter, self.active_on_weekdays)

        name = self.__class__.__name__
        return name + "(is_active=" + str(self.is_active) + ", active_on_weekdays=" + active_on_weekdays + ", start_hour=" + str(self.start_hour) + ", start_minute=" + str(self.start_minute) + ", end_hour=" + str(self.end_hour) + ", end_minute=" + str(self.end_minute) + ")"


class RandomModeSetNotification(AbstractCommandConfirmationNotification):
    pass


class DeviceNameSetNotification(AbstractCommandConfirmationNotification):
    pass


class DeviceSerialRequestedNotification:
    def __init__(self, serial):
        self.serial = serial

    def __str__(self):
        name = self.__class__.__name__
        return name + "(serial=" + str(self.serial) + ")"


class MeasurementRequestedNotification:
    def __init__(self, is_power_active, power_in_milliwatt, voltage_in_volt, current_in_milliampere, frequency_in_hertz, total_consumption_in_kilowatt_hour):
        self.is_power_active = is_power_active
        self.power_in_milliwatt = power_in_milliwatt
        self.voltage_in_volt = voltage_in_volt
        self.current_in_milliampere = current_in_milliampere
        self.frequency_in_hertz = frequency_in_hertz
        self.total_consumption_in_kilowatt_hour = total_consumption_in_kilowatt_hour

    def __str__(self):
        name = self.__class__.__name__
        return name + "(is_power_active=" + str(self.is_power_active) + ", power_in_milliwatt=" + str(self.power_in_milliwatt) + ", voltage_in_volt=" + str(self.voltage_in_volt) + ", current_in_milliampere=" + str(self.current_in_milliampere) + ", frequency_in_hertz=" + str(self.frequency_in_hertz) + ", total_consumption_in_kilowatt_hour=" + str(self.total_consumption_in_kilowatt_hour) + ")"

