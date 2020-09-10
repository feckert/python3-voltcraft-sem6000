from .message import *
from . import util

import datetime
import sys

class InvalidPayloadLengthException(Exception):
    def __init__(self, message_class, expected_payload_length, actual_payload_length):
        self.message_class = message_class
        self.expected_payload_length = expected_payload_length
        self.actual_payload_length = actual_payload_length

    def __str__(self):
        return "message has invalid payload length for " + self.message_class.__name__ +  " (expected: " + str(self.expected_payload_length) + ", actual=" + str(self.actual_payload_length) + ")"

class MessageParser:
    def __init__(self, year_diff=None):
        # the device only operates with two digit years
        # determine or set the difference to the current 4 digit year
        if year_diff is None:
            self.year_diff = (datetime.datetime.now().year % 100) * 100
        else:
            self.year_diff = year_diff

    def _parse_payload(self, data):
        if data[0:1] != b'\x0f':
            raise Exception("Invalid response")

        length_of_payload = data[1]

        payload = data[2:2+length_of_payload-1]
        checksum_received = data[2+length_of_payload-1]

        checksum = (1+sum(payload)) & 0xff

        if checksum_received != checksum:
            raise Exception("Invalid checksum: actual=" + str(checksum) + ", received=" + str(checksum_received))

        if len(data) > 2+length_of_payload:
            # if suffix exists it must be b'\xff\xff'
            suffix = data[2+length_of_payload:]
            if suffix != b'\xff\xff':
                raise Exception("Invalid suffix " + str(suffix))

        return payload

    def _parse_scheduler(self, data):
        is_active = False
        if data[0:1] == b'\x01':
            is_active = True

        is_action_turn_on = False
        if data[1:2] == b'\x01':
            is_action_turn_on = True

        repeat_on_weekdays_mask = int.from_bytes(data[2:3], 'big')
        repeat_on_weekdays = []
        for w in range(7):
            if repeat_on_weekdays_mask & 2**w:
                repeat_on_weekdays.append(w)

        # only the last two digits are returned for the year
        year = int.from_bytes(data[3:4], 'big') + self.year_diff
        month = int.from_bytes(data[4:5], 'big')
        day  = int.from_bytes(data[5:6], 'big')
        hour = int.from_bytes(data[6:7], 'big')
        minute = int.from_bytes(data[7:8], 'big')

        d = datetime.datetime(year, month, day, hour, minute)

        if len(repeat_on_weekdays):
            return RepeatedScheduler(
                is_active=is_active, 
                is_action_turn_on=is_action_turn_on, 
                repeat_on_weekdays=repeat_on_weekdays, 
                isotime=d.time().isoformat(timespec='minutes'))
        else:
            return OneTimeScheduler(
                is_active=is_active, 
                is_action_turn_on=is_action_turn_on, 
                isodatetime=d.isoformat(timespec='minutes'))

    def parse(self, data):
        payload = self._parse_payload(data)

        if payload[0:2] == b'\x17\x00' and payload[3:4] == b'\x00':
            if len(payload) != 5:
                raise InvalidPayloadLengthException(message_class=AuthenticationNotification.__class__, expected_payload_length=5, actual_payload_length=len(payload))

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True

            return AuthorizedNotification(was_successful=was_successful)

        if payload[0:2] == b'\x17\x00' and payload[3:4] == b'\x01':
            if len(payload) != 5:
                raise InvalidPayloadLengthException(message_class=PinChangedNotification.__class__, expected_payload_length=5, actual_payload_length=len(payload))

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True
            
            return PinChangedNotification(was_successful=was_successful)

        if payload[0:2] == b'\x17\x00' and payload[3:4] == b'\x02':
            if len(payload) != 5:
                raise InvalidPayloadLengthException(message_class=PinResetNotification.__class__, expected_payload_length=5, actual_payload_length=len(payload))

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True

            return PinResetNotification(was_successful=was_successful)

        if payload[0:2] == b'\x03\x00':
            if len(payload) != 3:
                raise InvalidPayloadLengthException(message_class=PowerSwitchedNotification.__class__, expected_payload_length=3, actual_payload_length=len(payload))

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True

            return PowerSwitchedNotification(was_successful=was_successful)

        if payload[0:3] == b'\x0f\x00\x05':
            if len(payload) != 4:
                raise InvalidPayloadLengthException(message_class=NightmodeChangedNotification.__class__, expected_payload_length=4, actual_payload_length=len(payload))

            return NightmodeChangedNotification(was_successful=True)

        if payload[0:2] == b'\x01\x00':
            if len(payload) != 3:
                raise InvalidPayloadLengthException(message_class=DateAndTimeChangedNotification.__class__, expected_payload_length=3, actual_payload_length=len(payload))

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True

            return DateAndTimeChangedNotification(was_successful=was_successful)

        if payload[0:2] == b'\x10\x00':
            if len(payload) != 13:
                raise InvalidPayloadLengthException(message_class=SettingsRequestedNotification.__class__, expected_payload_length=13, actual_payload_length=len(payload))

            is_reduced_period = False
            if payload[2:3] == b'\x01':
                is_reduced_period = True

            normal_price_in_cent = int.from_bytes(payload[3:4], 'big')
            reduced_period_price_in_cent = int.from_bytes(payload[4:5], 'big')

            reduced_period_start_time_in_minutes = int.from_bytes(payload[5:7], 'big')
            reduced_period_end_time_in_minutes = int.from_bytes(payload[7:9], 'big')

            reduced_period_start_time = util._parse_time_from_minutes(reduced_period_start_time_in_minutes)
            reduced_period_end_time = util._parse_time_from_minutes(reduced_period_end_time_in_minutes)

            is_nightmode_active = True
            if payload[9:10] == b'\x01':
                is_nightmode_active = False

            power_limit_in_watt = int.from_bytes(payload[11:13], 'big')

            return SettingsRequestedNotification(is_reduced_period=is_reduced_period, normal_price_in_cent=normal_price_in_cent, reduced_period_price_in_cent=reduced_period_price_in_cent, reduced_period_start_isotime=reduced_period_start_time.isoformat(timespec='minutes'), reduced_period_end_isotime=reduced_period_end_time.isoformat('minutes'), is_nightmode_active=is_nightmode_active, power_limit_in_watt=power_limit_in_watt)

        if payload[0:3] == b'\x05\x00\x00' and len(payload) == 3:
            return PowerLimitChangedNotification(was_successful=True)

        if payload[0:3] == b'\x0f\x00\x04':
            if len(payload) != 4:
                raise InvalidPayloadLengthException(message_class=PricesChangedNotification.__class__, expected_payload_length=4, actual_payload_length=len(payload))

            return PricesChangedNotification(was_successful=True)

        if payload[0:3] == b'\x0f\x00\x01':
            if len(payload) != 4:
                raise InvalidPayloadLengthException(message_class=ReducedPeriodChangedNotification.__class__, expected_payload_length=4, actual_payload_length=len(payload))

            return ReducedPeriodChangedNotification(was_successful=True)

        if payload[0:2] == b'\x09\x00':
            if len(payload) != 13:
                raise InvalidPayloadLengthException(message_class=TimerStatusRequestedNotification.__class__, expected_payload_length=13, actual_payload_length=len(payload))

            is_active = False 
            is_action_turn_on = False

            if payload[2:3] == b'\x01':
                is_active = True
                is_action_turn_on = True
            if payload[2:3] == b'\x02':
                is_active = True

            target_second = payload[3]
            target_minute = payload[4]
            target_hour = payload[5]
            target_day = payload[6]
            target_month = payload[7]
            # only the last two digits are returned for the year
            target_year = payload[8] + self.year_diff

            original_timer_length_in_seconds = int.from_bytes(payload[9:12], 'big')

            if target_year and target_month and target_day:
                d = datetime.datetime(target_year, target_month, target_day, target_hour, target_minute, target_second)
            else:
                d = datetime.datetime(1970, 1, 1, target_hour, target_minute, target_second)

            return TimerStatusRequestedNotification(is_active=is_active, is_action_turn_on=is_action_turn_on, target_isodatetime=d.isoformat(timespec='seconds'), original_timer_length_in_seconds=original_timer_length_in_seconds)

        if payload[0:2] == b'\x08\x00':
            if len(payload) != 3:
                raise InvalidPayloadLengthException(message_class=TimerSetNotification, expected_payload_length=3, actual_payload_length=len(payload))

            return TimerSetNotification(was_successful=True)

        if payload[0:2] == b'\x14\x00':
            if len(payload) < 3:
                raise InvalidPayloadLengthException(message_class=SchedulerRequestedNotification, expected_payload_length=3, actual_payload_length=len(payload))
            if (len(payload)-3) % 12 != 0:
                expected = len(payload) + 12 - (len(payload)-3) % 12
                raise InvalidPayloadLengthException(message_class=SchedulerRequestedNotification, expected_payload_length=expected, actual_payload_length=len(payload))

            number_of_schedulers = int.from_bytes(payload[2:3], 'big')
            number_of_schedulers_in_message = (len(payload)-3)//12

            scheduler_entries = []
            for i in range(number_of_schedulers_in_message):
                slot_id = int.from_bytes(payload[3 + i*12:4 + i*12], 'big')

                checksum_received = int.from_bytes(payload[14 + i*12:15 + i*12], 'big')
                checksum = (sum(payload[4 + i*12:14 + i*12])+0x14) & 0xff

                if checksum_received != checksum:
                    # TODO: how to calculate the correct checksum?
                    print("Invalid checksum for scheduler " + str(slot_id) + ": actual=" + str(checksum) + ", received=" + str(checksum_received), file=sys.stderr)
                    # raise Exception("Invalid checksum for scheduler " + str(slot_id) + ": actual=" + str(checksum) + ", received=" + str(checksum_received))

                scheduler = self._parse_scheduler(payload[4 + i*12:12 + i*12])

                scheduler_entries.append(SchedulerEntry(slot_id=slot_id, scheduler=scheduler))

            return SchedulerRequestedNotification(number_of_schedulers=number_of_schedulers, scheduler_entries=scheduler_entries)

        if payload[0:2] == b'\x13\x00':
            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True

            return SchedulerChangedNotification(was_successful=was_successful)

        if payload[0:2] == b'\x16\x00':
            is_active = False
            if payload[2:3] == b'\x01':
                is_active = True

            active_on_weekdays_mask = int.from_bytes(payload[3:4], 'big')
            active_on_weekdays = []
            for w in range(7):
                if active_on_weekdays_mask & 2**w:
                    active_on_weekdays.append(w)

            start_hour = int.from_bytes(payload[4:5], 'big')
            start_minute = int.from_bytes(payload[5:6], 'big')
            end_hour = int.from_bytes(payload[6:7], 'big')
            end_minute = int.from_bytes(payload[7:8], 'big')

            start_time = datetime.time(start_hour, start_minute)
            end_time = datetime.time(end_hour, end_minute)

            return RandomModeStatusRequestedNotification(is_active=is_active, active_on_weekdays=active_on_weekdays, start_isotime=start_time.isoformat(timespec='minutes'), end_isotime=end_time.isoformat(timespec='minutes'))

        if payload[0:2] == b'\x15\x00':
            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True

            return RandomModeChangedNotification(was_successful=was_successful)

        if payload[0:2] == b'\x04\x00':
            is_power_active = False
            if payload[2:3] == b'\x01':
                is_power_active = True

            power_in_milliwatt = int.from_bytes(payload[3:6], 'big')
            voltage_in_volt = int.from_bytes(payload[6:7], 'big')
            current_in_milliampere = int.from_bytes(payload[7:9], 'big')
            frequency_in_hertz = int.from_bytes(payload[9:10], 'big')
            total_consumption_in_kilowatt_hour = int.from_bytes(payload[12:16], 'big')

            return MeasurementRequestedNotification(is_power_active=is_power_active, power_in_milliwatt=power_in_milliwatt, voltage_in_volt=voltage_in_volt, current_in_milliampere=current_in_milliampere, frequency_in_hertz=frequency_in_hertz, total_consumption_in_kilowatt_hour=total_consumption_in_kilowatt_hour)

        if payload[0:2] == b'\x0c\x00':
            consumptions = []
            for i in range((len(payload)-2) // 4):
                consumptions.insert(0, int.from_bytes(payload[2 + 4*i:2 + 4*i + 3], 'big'))

            # notification does not contain measurement for current month
            consumptions.insert(0, None)

            return ConsumptionOfLast12MonthsRequestedNotification(consumption_n_months_ago_in_watt_hour=consumptions)

        if payload[0:2] == b'\x0b\x00':
            consumptions = []
            for i in range((len(payload)-2) // 4):
                consumptions.insert(0, int.from_bytes(payload[2 + 4*i:2 + 4*i + 3], 'big'))

            # notification does not contain measurement for today
            consumptions.insert(0, None)

            return ConsumptionOfLast30DaysRequestedNotification(consumption_n_days_ago_in_watt_hour=consumptions)

        if payload[0:2] == b'\x0a\x00':
            consumptions = []
            for i in range((len(payload)-2) // 2):
                consumptions.insert(0, int.from_bytes(payload[2 + 2*i:2 + 2*(i+1)], 'big'))

            return ConsumptionOfLast23HoursRequestedNotification(consumption_n_hours_ago_in_watt_hour=consumptions)

        if payload[0:3] == b'\x0f\x00\x02':
            return ConsumptionResetNotification(was_successful=True)

        if payload[0:3] == b'\x0f\x00\x00':
            return FactoryResetNotification(was_successful=True)

        if payload[0:2] == b'\x02\x00':
            return DeviceNameChangedNotification(was_successful=True)

        if payload[0:2] == b'\x11\x00':
            serial = payload[2:-2].decode('utf-8')

            return DeviceSerialRequestedNotification(serial=serial)

        raise Exception('Unsupported message')
