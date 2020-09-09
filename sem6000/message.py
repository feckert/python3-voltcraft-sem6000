from . import util

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


class NightmodeSetCommand(AbstractSwitchCommand):
    pass


class SynchronizeDateAndTimeCommand():
    def __init__(self, isodatetime):
        d = datetime.datetime.fromisoformat(isodatetime)
        self.isodatetime = d.isoformat(timespec='seconds')

    def __str__(self):
        name = self.__class__.__name__
        return name + "(isodatetime=" + str(self.isodatetime) + ")"


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
    def __init__(self, is_active, start_isotime, end_isotime):
        self.is_active = is_active
        self.start_isotime = start_isotime
        self.end_isotime = end_isotime

    def __str__(self):
        name = self.__class__.__name__
        return name + "(is_active=" + str(self.is_active) + ", start_isotime=" + str(self.start_isotime) + ", end_isotime=" + str(self.end_isotime) + ")"


class RequestTimerStatusCommand(AbstractCommand):
    pass


class SetTimerCommand:
    def __init__(self, is_reset_timer, is_action_turn_on, target_isodatetime=None):
        if not is_reset_timer and target_isodatetime is None:
            raise Exception("target_isodatetime parameter is None")

        if is_reset_timer and not target_isodatetime is None:
            raise Exception("target_isodatetime parameter is expected to be None if timer is being reset")

        self.is_reset_timer = is_reset_timer
        self.is_action_turn_on = is_action_turn_on
        self.target_isodatetime = None

        if not is_reset_timer:
            d = datetime.datetime.fromisoformat(target_isodatetime)
            self.target_isodatetime = d.isoformat(timespec='seconds')

    def __str__(self):
        name = self.__class__.__name__
        return name + "(is_reset_timer=" + str(self.is_reset_timer) + ", is_action_turn_on=" + str(self.is_action_turn_on) + ", target_isodatetime=" + str(self.target_isodatetime) + ")"


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
    def __init__(self, is_active, active_on_weekdays, start_isotime, end_isotime):
        active_on_weekdays = util._list_values_to_enum(util.Weekday, active_on_weekdays)

        self.is_active = is_active
        self.active_on_weekdays = active_on_weekdays

        start_time = datetime.time.fromisoformat(start_isotime)
        end_time = datetime.time.fromisoformat(end_isotime)

        self.start_isotime = start_time.isoformat(timespec='minutes')
        self.end_isotime = end_time.isoformat(timespec='minutes')

    def __str__(self):
        weekday_formatter = lambda w: w.name
        active_on_weekdays = util._format_list_of_objects(weekday_formatter, self.active_on_weekdays)

        name = self.__class__.__name__
        return name + "(is_active=" + str(self.is_active) + ", active_on_weekdays=" + active_on_weekdays + ", start_isotime=" + str(self.start_isotime) + ", end_isotime=" + str(self.end_isotime) + ")"


class RequestMeasurementCommand(AbstractCommand):
    pass


class RequestConsumptionOfLast12MonthsCommand(AbstractCommand):
    pass


class RequestConsumptionOfLast30DaysCommand(AbstractCommand):
    pass


class RequestConsumptionOfLast23HoursCommand(AbstractCommand):
    pass


class ResetConsumptionCommand(AbstractCommand):
    pass


class FactoryResetCommand(AbstractCommand):
    pass


class SetDeviceNameCommand:
        def __init__(self, new_name):
            self.new_name = new_name

        def __str__(self):
            command = self.__class__.__name__
            return command + "(new_name=" + str(self.new_name) + ")"


class RequestDeviceSerialCommand(AbstractCommand):
    pass


class AuthorizedNotification(AbstractCommandConfirmationNotification):
    pass


class PinChangedNotification(AbstractCommandConfirmationNotification):
    pass


class PinResetNotification(AbstractCommandConfirmationNotification):
    pass


class PowerSwitchedNotification(AbstractCommandConfirmationNotification):
    pass


class NightmodeSetNotification(AbstractCommandConfirmationNotification):
    pass


class DateAndTimeSetNotification(AbstractCommandConfirmationNotification):
    pass


class SettingsRequestedNotification:
    def __init__(self, is_reduced_period, normal_price_in_cent, reduced_period_price_in_cent, reduced_period_start_isotime, reduced_period_end_isotime, is_nightmode_active, power_limit_in_watt):
        self.is_reduced_period = is_reduced_period
        self.normal_price_in_cent = normal_price_in_cent
        self.reduced_period_price_in_cent = reduced_period_price_in_cent

        start_time = datetime.time.fromisoformat(reduced_period_start_isotime)
        end_time = datetime.time.fromisoformat(reduced_period_end_isotime)

        self.reduced_period_start_isotime = start_time.isoformat(timespec='minutes')
        self.reduced_period_end_isotime = end_time.isoformat(timespec='minutes')

        self.is_nightmode_active = is_nightmode_active
        self.power_limit_in_watt = power_limit_in_watt

    def __str__(self):
        name = self.__class__.__name__
        return name + "(is_reduced_period=" + str(self.is_reduced_period) + ", normal_price_in_cent=" + str(self.normal_price_in_cent) + ", reduced_periiod_price_in_cent=" + str(self.reduced_period_price_in_cent) + ", reduced_period_start_isotime=" + str(self.reduced_period_start_isotime) + ", reduced_period_end_isotime=" + str(self.reduced_period_end_isotime) + ", is_nightmode_active=" + str(self.is_nightmode_active) + ", power_limit_in_watt=" + str(self.power_limit_in_watt) + ")"


class PowerLimitSetNotification(AbstractCommandConfirmationNotification):
    pass


class PricesSetNotification(AbstractCommandConfirmationNotification):
    pass


class ReducedPeriodSetNotification(AbstractCommandConfirmationNotification):
    pass


class TimerStatusRequestedNotification:
    def __init__(self, is_active, is_action_turn_on, target_isodatetime, original_timer_length_in_seconds):
        d = datetime.datetime.fromisoformat(target_isodatetime)

        self.is_active = is_active
        self.is_action_turn_on = is_action_turn_on
        self.target_isodatetime = d.isoformat(timespec='seconds')
        self.original_timer_length_in_seconds = original_timer_length_in_seconds

    def __str__(self):
        name = self.__class__.__name__
        return name + "(is_active=" + str(self.is_active) + ", is_action_turn_on=" + str(self.is_action_turn_on) + ", target_isodatetime=" + str(self.target_isodatetime) + ", original_timer_length_in_seconds=" + str(self.original_timer_length_in_seconds) + ")"


class TimerSetNotification(AbstractCommandConfirmationNotification):
    pass


class Scheduler:
    def __init__(self, is_active, is_action_turn_on, repeat_on_weekdays, isodatetime):

        repeat_on_weekdays = util._list_values_to_enum(util.Weekday, repeat_on_weekdays)

        self.is_active = is_active
        self.is_action_turn_on = is_action_turn_on
        self.repeat_on_weekdays = repeat_on_weekdays

        d = datetime.datetime.fromisoformat(isodatetime)
        self.isodatetime = d.isoformat(timespec='minutes')


class OneTimeScheduler(Scheduler):
    def __init__(self, is_active, is_action_turn_on, isodatetime):
        Scheduler.__init__(self, 
            is_active=is_active, 
            is_action_turn_on=is_action_turn_on,
            repeat_on_weekdays=[], 
            isodatetime=isodatetime)

    def __str__(self):
        name = self.__class__.__name__

        weekday_formatter = lambda w: w.name
        repeat_on_weekdays = util._format_list_of_objects(weekday_formatter, self.repeat_on_weekdays)

        return name + "(is_active=" + str(self.is_active) + ", is_action_turn_on=" + str(self.is_action_turn_on) + ", isodatetime=" + str(self.isodatetime) + ")"


class RepeatedScheduler(Scheduler):
    def __init__(self, is_active, is_action_turn_on, repeat_on_weekdays, isotime):
        Scheduler.__init__(self, 
            is_active=is_active, 
            is_action_turn_on=is_action_turn_on,
            repeat_on_weekdays=repeat_on_weekdays, 
            isodatetime=datetime.date.today().isoformat() + 'T' + isotime)

    def __str__(self):
        name = self.__class__.__name__

        weekday_formatter = lambda w: w.name
        repeat_on_weekdays = util._format_list_of_objects(weekday_formatter, self.repeat_on_weekdays)

        isotime = datetime.datetime.fromisoformat(self.isodatetime).time().isoformat(timespec='minutes')

        return name + "(is_active=" + str(self.is_active) + ", is_action_turn_on=" + str(self.is_action_turn_on) + ", repeat_on_weekdays=" + repeat_on_weekdays + ", isotime=" + isotime + ")"


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

        scheduler_entries = util._format_list_of_objects(str, self.scheduler_entries)

        return name + "(number_of_schedulers=" + str(self.number_of_schedulers) + ", scheduler_entries=" + scheduler_entries + ")"


class SchedulerSetNotification(AbstractCommandConfirmationNotification):
    pass


class RandomModeStatusRequestedNotification:
    def __init__(self, is_active, active_on_weekdays, start_isotime, end_isotime):
        active_on_weekdays = util._list_values_to_enum(util.Weekday, active_on_weekdays)

        self.is_active = is_active
        self.active_on_weekdays = active_on_weekdays

        start_time = datetime.time.fromisoformat(start_isotime)
        end_time = datetime.time.fromisoformat(end_isotime)

        self.start_isotime = start_time.isoformat(timespec='minutes')
        self.end_isotime = end_time.isoformat(timespec='minutes')

    def __str__(self):
        weekday_formatter = lambda w: w.name
        active_on_weekdays = util._format_list_of_objects(weekday_formatter, self.active_on_weekdays)

        name = self.__class__.__name__
        return name + "(is_active=" + str(self.is_active) + ", active_on_weekdays=" + active_on_weekdays + ", start_isotime=" + str(self.start_isotime) + ", end_isotime=" + str(self.end_isotime) + ")"


class RandomModeSetNotification(AbstractCommandConfirmationNotification):
    pass


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


class ConsumptionOfLast12MonthsRequestedNotification:
    def __init__(self, consumption_n_months_ago_in_watt_hour):
        self.consumption_n_months_ago_in_watt_hour = consumption_n_months_ago_in_watt_hour

    def __str__(self):
        name = self.__class__.__name__
        return name + "(consumption_n_months_ago_in_watt_hour=" + util._format_list_of_objects(str, self.consumption_n_months_ago_in_watt_hour) + ")"


class ConsumptionOfLast30DaysRequestedNotification:
    def __init__(self, consumption_n_days_ago_in_watt_hour):
        self.consumption_n_days_ago_in_watt_hour = consumption_n_days_ago_in_watt_hour

    def __str__(self):
        name = self.__class__.__name__
        return name + "(consumption_n_days_ago_in_watt_hour=" + util._format_list_of_objects(str, self.consumption_n_days_ago_in_watt_hour) + ")"


class ConsumptionOfLast23HoursRequestedNotification:
    def __init__(self, consumption_n_hours_ago_in_watt_hour):
        self.consumption_n_hours_ago_in_watt_hour = consumption_n_hours_ago_in_watt_hour

    def __str__(self):
        name = self.__class__.__name__
        return name + "(consumption_n_hours_ago_in_watt_hour=" + util._format_list_of_objects(str, self.consumption_n_hours_ago_in_watt_hour) + ")"


class ConsumptionResetNotification(AbstractCommandConfirmationNotification):
    pass


class FactoryResetNotification(AbstractCommandConfirmationNotification):
    pass


class DeviceNameSetNotification(AbstractCommandConfirmationNotification):
    pass


class DeviceNameRequestedNotification:
    def __init__(self, device_name):
        self.device_name = device_name

    def __str__(self):
        name = self.__class__.name
        return name + "(device_name=" + self.device_name + ")"


class DeviceSerialRequestedNotification:
    def __init__(self, serial):
        self.serial = serial

    def __str__(self):
        name = self.__class__.__name__
        return name + "(serial=" + str(self.serial) + ")"

