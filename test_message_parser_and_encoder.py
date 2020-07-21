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
        schedulers=[]
        for i in range(12):
            repeat_on_weekdays = []
            repeat_on_weekdays.append(SchedulerWeekday.SUNDAY)
            repeat_on_weekdays.append(SchedulerWeekday.MONDAY)
            repeat_on_weekdays.append(SchedulerWeekday.TUESDAY)
            repeat_on_weekdays.append(SchedulerWeekday.WEDNESDAY)
            repeat_on_weekdays.append(SchedulerWeekday.THURSDAY)
            repeat_on_weekdays.append(SchedulerWeekday.FRIDAY)
            repeat_on_weekdays.append(SchedulerWeekday.SATURDAY)

            schedulers.append(Scheduler(is_active=True, is_action_turn_on=True, repeat_on_weekdays=repeat_on_weekdays, year=20, month=12, day=3, hour=12, minute=34))

        message = SchedulerRequestedNotification(number_of_schedulers=12, schedulers=schedulers)

        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(12, parsed_message.number_of_schedulers)
        self.assertEqual(12, len(parsed_message.schedulers))
        for i in range(12):
            repeat_on_weekday_expected = []
            repeat_on_weekday_expected.append(SchedulerWeekday.SUNDAY)
            repeat_on_weekday_expected.append(SchedulerWeekday.MONDAY)
            repeat_on_weekday_expected.append(SchedulerWeekday.TUESDAY)
            repeat_on_weekday_expected.append(SchedulerWeekday.WEDNESDAY)
            repeat_on_weekday_expected.append(SchedulerWeekday.THURSDAY)
            repeat_on_weekday_expected.append(SchedulerWeekday.FRIDAY)
            repeat_on_weekday_expected.append(SchedulerWeekday.SATURDAY)

            self.assertEqual(True, parsed_message.schedulers[i].is_active, 'is_active value differs on scheduler ' + str(i))
            self.assertEqual(True, parsed_message.schedulers[i].is_action_turn_on, 'is_action_turn_on value differs on scheduler ' + str(i))
            self.assertEqual(repeat_on_weekday_expected, parsed_message.schedulers[i].repeat_on_weekdays, 'repeat_on_weekdays value differs on scheduler ' + str(i))
            self.assertEqual(20, parsed_message.schedulers[i].year, 'year value differs on scheduler ' + str(i))
            self.assertEqual(12, parsed_message.schedulers[i].month, 'month value differs on scheduler ' + str(i))
            self.assertEqual(3, parsed_message.schedulers[i].day, 'day value differs on scheduler ' + str(i))
            self.assertEqual(12, parsed_message.schedulers[i].hour, 'hour value differs on scheduler ' + str(i))
            self.assertEqual(34, parsed_message.schedulers[i].minute, 'minute value differs on scheduler ' + str(i))

