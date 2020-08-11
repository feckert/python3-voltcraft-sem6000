import unittest

from sem6000.encoder import MessageEncoder
from sem6000.parser import MessageParser
from sem6000.message import *
from sem6000 import util

class MessagesTest(unittest.TestCase):
    def test_AuthorizationNotification(self):
        message = AuthorizationNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_ChangePinNotification(self):
        message = ChangePinNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_ResetPinNotification(self):
        message = ResetPinNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_PowerSwitchNotification(self):
        message = PowerSwitchNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_LEDSwitchNotification(self):
        message = LEDSwitchNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_SynchroizeDateAndTimeNotification(self):
        message = SynchronizeDateAndTimeNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_RequestedSettingsNotification(self):
        message = RequestedSettingsNotification(is_reduced_period=True, normal_price_in_cent=100, reduced_period_price_in_cent=50, reduced_period_start_isotime="22:00", reduced_period_end_isotime="05:00", is_led_active=True, power_limit_in_watt=500)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.is_reduced_period, 'reduced_period_is_active value differs')
        self.assertEqual(100, parsed_message.normal_price_in_cent, 'normal_price_in_cent value differs')
        self.assertEqual(50, parsed_message.reduced_period_price_in_cent, 'reduced_price value_in_cent differs')
        self.assertEqual("22:00", parsed_message.reduced_period_start_isotime, 'reduced_period_start_isotime value differs')
        self.assertEqual("05:00", parsed_message.reduced_period_end_isotime, 'reduced_period_end_isotime value differs')
        self.assertEqual(True, parsed_message.is_led_active, 'is_led_active value differs')
        self.assertEqual(500, parsed_message.power_limit_in_watt, 'power_limit_in_watt value differs')

    def test_PowerLimitSetNotification(self):
        message = PowerLimitSetNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_PricesSetNotification(self):
        message = PricesSetNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_ReducedPeriodSetNotification(self):
        message = ReducedPeriodSetNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_RequestedTimerStatusNotification(self):
        message = RequestedTimerStatusNotification(is_active=True, is_action_turn_on=True, target_isodatetime="2004-03-12T12:34:12", original_timer_length_in_seconds=42)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser(year_diff=2000).parse(encoded_message)

        self.assertEqual(True, parsed_message.is_active, 'is_active value differs')
        self.assertEqual(True, parsed_message.is_action_turn_on, 'is_action_turn_on value differs')
        self.assertEqual("2004-03-12T12:34:12", parsed_message.target_isodatetime, 'target_isodatetime value differs')
        self.assertEqual(42, parsed_message.original_timer_length_in_seconds, 'original_timer_length_in_seconds value differs')

    def test_TimerSetNotification(self):
        message = TimerSetNotification(was_successful=True)

        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_SchedulerRequestedNotification(self):
        scheduler_entries=[]
        for i in range(12):
            repeat_on_weekdays = []
            repeat_on_weekdays.append(util.Weekday.SUNDAY)
            repeat_on_weekdays.append(util.Weekday.MONDAY)
            repeat_on_weekdays.append(util.Weekday.TUESDAY)
            repeat_on_weekdays.append(util.Weekday.WEDNESDAY)
            repeat_on_weekdays.append(util.Weekday.THURSDAY)
            repeat_on_weekdays.append(util.Weekday.FRIDAY)
            repeat_on_weekdays.append(util.Weekday.SATURDAY)

            scheduler = Scheduler(is_active=True, is_action_turn_on=True, repeat_on_weekdays=repeat_on_weekdays, isodatetime="2020-12-03T12:34")
            scheduler_entries.append(SchedulerEntry(slot_id=i, scheduler=scheduler))

        message = SchedulerRequestedNotification(number_of_schedulers=12, scheduler_entries=scheduler_entries)

        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser(year_diff=2000).parse(encoded_message)

        self.assertEqual(12, parsed_message.number_of_schedulers)
        self.assertEqual(12, len(parsed_message.scheduler_entries))
        for i in range(12):
            repeat_on_weekday_expected = []
            repeat_on_weekday_expected.append(util.Weekday.SUNDAY)
            repeat_on_weekday_expected.append(util.Weekday.MONDAY)
            repeat_on_weekday_expected.append(util.Weekday.TUESDAY)
            repeat_on_weekday_expected.append(util.Weekday.WEDNESDAY)
            repeat_on_weekday_expected.append(util.Weekday.THURSDAY)
            repeat_on_weekday_expected.append(util.Weekday.FRIDAY)
            repeat_on_weekday_expected.append(util.Weekday.SATURDAY)

            self.assertEqual(i, parsed_message.scheduler_entries[i].slot_id, 'slot_id value differs on scheduler ' + str(i))
            self.assertEqual(True, parsed_message.scheduler_entries[i].scheduler.is_active, 'is_active value differs on scheduler ' + str(i))
            self.assertEqual(True, parsed_message.scheduler_entries[i].scheduler.is_action_turn_on, 'is_action_turn_on value differs on scheduler ' + str(i))
            self.assertEqual(repeat_on_weekday_expected, parsed_message.scheduler_entries[i].scheduler.repeat_on_weekdays, 'repeat_on_weekdays value differs on scheduler ' + str(i))
            self.assertEqual("2020-12-03T12:34", parsed_message.scheduler_entries[i].scheduler.isodatetime, 'isodatetime value differs on scheduler ' + str(i))

    def test_SchedulerSetNotification(self):
        message = SchedulerSetNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_RandomModeStatusRequestedNotification(self):
        active_on_weekdays=[]
        active_on_weekdays.append(util.Weekday.SUNDAY)
        active_on_weekdays.append(util.Weekday.MONDAY)
        active_on_weekdays.append(util.Weekday.TUESDAY)
        active_on_weekdays.append(util.Weekday.WEDNESDAY)
        active_on_weekdays.append(util.Weekday.THURSDAY)
        active_on_weekdays.append(util.Weekday.FRIDAY)
        active_on_weekdays.append(util.Weekday.SATURDAY)

        message = RandomModeStatusRequestedNotification(is_active=True, active_on_weekdays=active_on_weekdays, start_isotime="10:30", end_isotime="18:45")
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        active_on_weekdays_expected=[]
        active_on_weekdays_expected.append(util.Weekday.SUNDAY)
        active_on_weekdays_expected.append(util.Weekday.MONDAY)
        active_on_weekdays_expected.append(util.Weekday.TUESDAY)
        active_on_weekdays_expected.append(util.Weekday.WEDNESDAY)
        active_on_weekdays_expected.append(util.Weekday.THURSDAY)
        active_on_weekdays_expected.append(util.Weekday.FRIDAY)
        active_on_weekdays_expected.append(util.Weekday.SATURDAY)

        self.assertEqual(True, parsed_message.is_active, 'is_active value differs')
        self.assertEqual(active_on_weekdays_expected, parsed_message.active_on_weekdays, 'active_on_weekdays value differs')
        self.assertEqual("10:30", parsed_message.start_isotime, 'start_isotime value differs')
        self.assertEqual("18:45", parsed_message.end_isotime, 'end_isotime value differs')

    def test_RandomModeSetNotification(self):
        message = RandomModeSetNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_MeasurementRequestedNotification(self):
        message = MeasurementRequestedNotification(is_power_active=True, power_in_milliwatt=80, voltage_in_volt=230, current_in_milliampere=1000, frequency_in_hertz=50, total_consumption_in_kilowatt_hour=1000)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.is_power_active, 'is_power_active value differs')
        self.assertEqual(80, parsed_message.power_in_milliwatt, 'power_in_milliwatt value differs')
        self.assertEqual(230, parsed_message.voltage_in_volt, 'voltage_in_volt value differs')
        self.assertEqual(1000, parsed_message.current_in_milliampere, 'current_in_milliampere value differs')
        self.assertEqual(50, parsed_message.frequency_in_hertz, 'frequency_in_hertz value differs')
        self.assertEqual(1000, parsed_message.total_consumption_in_kilowatt_hour, 'total_consumption_in_kilowatt_hour value differs')

    def test_ConsumptionOfLast12MonthsRequestedNotification(self):
        message = ConsumptionOfLast12MonthsRequestedNotification(consumption_n_months_ago_in_watt_hour=[None, 10,20,30,40,50,60,70,80,90,100,110,120])
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(13, len(parsed_message.consumption_n_months_ago_in_watt_hour), 'incorrect number of values')
        self.assertEqual([None, 10,20,30,40,50,60,70,80,90,100,110,120], parsed_message.consumption_n_months_ago_in_watt_hour, 'values for consumption in watt hour differ')

    def test_ConsumptionOfLast30DaysRequestedNotification(self):
        message = ConsumptionOfLast30DaysRequestedNotification(consumption_n_days_ago_in_watt_hour=[None, 10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300])
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(31, len(parsed_message.consumption_n_days_ago_in_watt_hour), 'number of values differ')
        self.assertEqual([None, 10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300], parsed_message.consumption_n_days_ago_in_watt_hour, 'values for consumption in watt hour differ')

    def test_ConsumptionOfLast23HoursRequestedNotification(self):
        message = ConsumptionOfLast23HoursRequestedNotification(consumption_n_hours_ago_in_watt_hour=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240])
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(24, len(parsed_message.consumption_n_hours_ago_in_watt_hour), 'number of values differ')
        self.assertEqual([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240], parsed_message.consumption_n_hours_ago_in_watt_hour, 'values for consumption in watt hour differ')

    def test_ResetConsumptionNotification(self):
        message = ResetConsumptionNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_FactoryResetNotification(self):
        message = FactoryResetNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_DeviceNameSetNotification(self):
        message = DeviceNameSetNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_DeviceSerialRequestedNotification(self):
        message = DeviceSerialRequestedNotification("ML01D10012000000")
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual("ML01D10012000000", message.serial, 'serial value differs')


