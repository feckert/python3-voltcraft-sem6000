import unittest

from encoder import MessageEncoder
from parser import MessageParser
from message import *

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
        message = RequestedSettingsNotification(is_reduced_mode_active=True, normal_price_in_cent=100, reduced_price_in_cent=50, reduced_mode_start_time_in_minutes=1320, reduced_mode_end_time_in_minutes=300, is_led_active=True, power_limit_in_watt=500)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.is_reduced_mode_active, 'reduced_mode_is_active value differs')
        self.assertEqual(100, parsed_message.normal_price_in_cent, 'normal_price_in_cent value differs')
        self.assertEqual(50, parsed_message.reduced_price_in_cent, 'reduced_price value_in_cent differs')
        self.assertEqual(1320, parsed_message.reduced_mode_start_time_in_minutes, 'reduced_mode_start_time_in_minutes value differs')
        self.assertEqual(300, parsed_message.reduced_mode_end_time_in_minutes, 'reduced_mode_end_time_in_minutes value differs')
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
        message = RequestedTimerStatusNotification(is_timer_running=True, is_action_turn_on=True, target_second=12, target_minute=34, target_hour=12, target_day=12, target_month=3, target_year=4, original_timer_length_in_seconds=42)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.is_timer_running, 'is_timer_running value differs')
        self.assertEqual(True, parsed_message.is_action_turn_on, 'is_action_turn_on value differs')
        self.assertEqual(12, parsed_message.target_second, 'target_second value differs')
        self.assertEqual(34, parsed_message.target_minute, 'target_minute value differs')
        self.assertEqual(12, parsed_message.target_hour, 'target_hour value differs')
        self.assertEqual(12, parsed_message.target_day, 'target_day value differs')
        self.assertEqual(3, parsed_message.target_month, 'target_month value differs')
        self.assertEqual(4, parsed_message.target_year, 'target_year value differs')
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
            repeat_on_weekdays.append(Weekday.SUNDAY)
            repeat_on_weekdays.append(Weekday.MONDAY)
            repeat_on_weekdays.append(Weekday.TUESDAY)
            repeat_on_weekdays.append(Weekday.WEDNESDAY)
            repeat_on_weekdays.append(Weekday.THURSDAY)
            repeat_on_weekdays.append(Weekday.FRIDAY)
            repeat_on_weekdays.append(Weekday.SATURDAY)

            scheduler = Scheduler(is_active=True, is_action_turn_on=True, repeat_on_weekdays=repeat_on_weekdays, year=20, month=12, day=3, hour=12, minute=34)
            scheduler_entries.append(SchedulerEntry(slot_id=i, scheduler=scheduler))

        message = SchedulerRequestedNotification(number_of_schedulers=12, scheduler_entries=scheduler_entries)

        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(12, parsed_message.number_of_schedulers)
        self.assertEqual(12, len(parsed_message.scheduler_entries))
        for i in range(12):
            repeat_on_weekday_expected = []
            repeat_on_weekday_expected.append(Weekday.SUNDAY)
            repeat_on_weekday_expected.append(Weekday.MONDAY)
            repeat_on_weekday_expected.append(Weekday.TUESDAY)
            repeat_on_weekday_expected.append(Weekday.WEDNESDAY)
            repeat_on_weekday_expected.append(Weekday.THURSDAY)
            repeat_on_weekday_expected.append(Weekday.FRIDAY)
            repeat_on_weekday_expected.append(Weekday.SATURDAY)

            self.assertEqual(i, parsed_message.scheduler_entries[i].slot_id, 'slot_id value differs on scheduler ' + str(i))
            self.assertEqual(True, parsed_message.scheduler_entries[i].scheduler.is_active, 'is_active value differs on scheduler ' + str(i))
            self.assertEqual(True, parsed_message.scheduler_entries[i].scheduler.is_action_turn_on, 'is_action_turn_on value differs on scheduler ' + str(i))
            self.assertEqual(repeat_on_weekday_expected, parsed_message.scheduler_entries[i].scheduler.repeat_on_weekdays, 'repeat_on_weekdays value differs on scheduler ' + str(i))
            self.assertEqual(20, parsed_message.scheduler_entries[i].scheduler.year, 'year value differs on scheduler ' + str(i))
            self.assertEqual(12, parsed_message.scheduler_entries[i].scheduler.month, 'month value differs on scheduler ' + str(i))
            self.assertEqual(3, parsed_message.scheduler_entries[i].scheduler.day, 'day value differs on scheduler ' + str(i))
            self.assertEqual(12, parsed_message.scheduler_entries[i].scheduler.hour, 'hour value differs on scheduler ' + str(i))
            self.assertEqual(34, parsed_message.scheduler_entries[i].scheduler.minute, 'minute value differs on scheduler ' + str(i))

    def test_SchedulerSetNotification(self):
        message = SchedulerSetNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_RandomModeStatusRequestedNotification(self):
        active_on_weekdays=[]
        active_on_weekdays.append(Weekday.SUNDAY)
        active_on_weekdays.append(Weekday.MONDAY)
        active_on_weekdays.append(Weekday.TUESDAY)
        active_on_weekdays.append(Weekday.WEDNESDAY)
        active_on_weekdays.append(Weekday.THURSDAY)
        active_on_weekdays.append(Weekday.FRIDAY)
        active_on_weekdays.append(Weekday.SATURDAY)

        message = RandomModeStatusRequestedNotification(is_active=True, active_on_weekdays=active_on_weekdays, start_hour=10, start_minute=30, end_hour=18, end_minute=45)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        active_on_weekdays_expected=[]
        active_on_weekdays_expected.append(Weekday.SUNDAY)
        active_on_weekdays_expected.append(Weekday.MONDAY)
        active_on_weekdays_expected.append(Weekday.TUESDAY)
        active_on_weekdays_expected.append(Weekday.WEDNESDAY)
        active_on_weekdays_expected.append(Weekday.THURSDAY)
        active_on_weekdays_expected.append(Weekday.FRIDAY)
        active_on_weekdays_expected.append(Weekday.SATURDAY)

        self.assertEqual(True, parsed_message.is_active, 'is_active value differs')
        self.assertEqual(active_on_weekdays_expected, parsed_message.active_on_weekdays, 'active_on_weekdays value differs')
        self.assertEqual(10, parsed_message.start_hour, 'start_hour value differs')
        self.assertEqual(30, parsed_message.start_minute, 'start_minute value differs')
        self.assertEqual(18, parsed_message.end_hour, 'end_hour value differs')
        self.assertEqual(45, parsed_message.end_minute, 'end_minute value differs')

    def test_RandomModeSetNotification(self):
        message = RandomModeSetNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_DeviceNameSetNotification(self):
        message = DeviceNameSetNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')
