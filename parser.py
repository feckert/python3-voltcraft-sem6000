from message import *

import sys

class InvalidPayloadLengthException(Exception):
    def __init__(self, message_class, expected_payload_length, actual_payload_length):
        self.message_class = message_class
        self.expected_payload_length = expected_payload_length
        self.actual_payload_length = actual_payload_length

    def __str__(self):
        return "message has invalid payload length for " + self.message_class.__name__ +  " (expected: " + str(self.expected_payload_length) + ", actual=" + str(self.actual_payload_length) + ")"

class MessageParser:
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

        year = int.from_bytes(data[3:4], 'big')
        month = int.from_bytes(data[4:5], 'big')
        day  = int.from_bytes(data[5:6], 'big')
        hour = int.from_bytes(data[6:7], 'big')
        minute = int.from_bytes(data[7:8], 'big')

        return Scheduler(is_active=is_active, is_action_turn_on=is_action_turn_on, repeat_on_weekdays=repeat_on_weekdays, year=year, month=month, day=day, hour=hour, minute=minute)

    def parse(self, data):
        payload = self._parse_payload(data)

        if payload[0:2] == b'\x17\x00' and payload[3:4] == b'\x00':
            if len(payload) != 5:
                raise InvalidPayloadLengthException(message_class=AuthenticationNotification.__class__, expected_payload_length=5, actual_payload_length=len(payload))

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True

            return AuthorizationNotification(was_successful=was_successful)

        if payload[0:2] == b'\x17\x00' and payload[3:4] == b'\x01':
            if len(payload) != 5:
                raise InvalidPayloadLengthException(message_class=ChangePinNotification.__class__, expected_payload_length=5, actual_payload_length=len(payload))

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True
            
            return ChangePinNotification(was_successful=was_successful)

        if payload[0:2] == b'\x17\x00' and payload[3:4] == b'\x02':
            if len(payload) != 5:
                raise InvalidPayloadLengthException(message_class=ResetPinNotification.__class__, expected_payload_length=5, actual_payload_length=len(payload))

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True

            return ResetPinNotification(was_successful=was_successful)

        if payload[0:2] == b'\x03\x00':
            if len(payload) != 3:
                raise InvalidPayloadLengthException(message_class=PowerSwitchNotification.__class__, expected_payload_length=3, actual_payload_length=len(payload))

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True

            return PowerSwitchNotification(was_successful=was_successful)

        if payload[0:3] == b'\x0f\x00\x05':
            if len(payload) != 4:
                raise InvalidPayloadLengthException(message_class=LEDSwitchNotification.__class__, expected_payload_length=4, actual_payload_length=len(payload))

            return LEDSwitchNotification(was_successful=True)

        if payload[0:2] == b'\x01\x00':
            if len(payload) != 3:
                raise InvalidPayloadLengthException(message_class=SynchronizeDateAndTimeNotification.__class__, expected_payload_length=3, actual_payload_length=len(payload))

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True

            return SynchronizeDateAndTimeNotification(was_successful=was_successful)

        if payload[0:2] == b'\x10\x00':
            if len(payload) != 13:
                raise InvalidPayloadLengthException(message_class=RequestedSettingsNotification.__class__, expected_payload_length=13, actual_payload_length=len(payload))

            is_reduced_mode_active = False
            if payload[2:3] == b'\x01':
                is_reduced_mode_active = True

            normal_price_in_cent = int.from_bytes(payload[3:4], 'big')
            reduced_price_in_cent = int.from_bytes(payload[4:5], 'big')

            reduced_mode_start_time_in_minutes = int.from_bytes(payload[5:7], 'big')
            reduced_mode_end_time_in_minutes = int.from_bytes(payload[7:9], 'big')

            is_led_active = False
            if payload[9:10] == b'\x01':
                is_led_active = True

            power_limit_in_watt = int.from_bytes(payload[11:13], 'big')

            return RequestedSettingsNotification(is_reduced_mode_active=is_reduced_mode_active, normal_price_in_cent=normal_price_in_cent, reduced_price_in_cent=reduced_price_in_cent, reduced_mode_start_time_in_minutes=reduced_mode_start_time_in_minutes, reduced_mode_end_time_in_minutes=reduced_mode_end_time_in_minutes, is_led_active=is_led_active, power_limit_in_watt=power_limit_in_watt)

        if payload[0:3] == b'\x05\x00\x00' and len(payload) == 3:
            return PowerLimitSetNotification(was_successful=True)

        if payload[0:3] == b'\x0f\x00\x04':
            if len(payload) != 4:
                raise InvalidPayloadLengthException(message_class=PricesSetNotification.__class__, expected_payload_length=4, actual_payload_length=len(payload))

            return PricesSetNotification(was_successful=True)

        if payload[0:3] == b'\x0f\x00\x01':
            if len(payload) != 4:
                raise InvalidPayloadLengthException(message_class=ReducedPeriodSetNotification.__class__, expected_payload_length=4, actual_payload_length=len(payload))

            return ReducedPeriodSetNotification(was_successful=True)

        if payload[0:2] == b'\x09\x00':
            if len(payload) != 13:
                raise InvalidPayloadLengthException(message_class=RequestedTimerStatusNotification.__class__, expected_payload_length=13, actual_payload_length=len(payload))

            is_timer_running = True
            is_action_turn_on = False

            if payload[2:3] == b'\x01':
                is_action_turn_on = True
            if payload[2:3] == b'\x00':
                is_timer_running = False

            target_second = payload[3]
            target_minute = payload[4]
            target_hour = payload[5]
            target_day = payload[6]
            target_month = payload[7]
            target_year = payload[8]

            original_timer_length_in_seconds = int.from_bytes(payload[9:12], 'big')

            return RequestedTimerStatusNotification(is_timer_running=is_timer_running, is_action_turn_on=is_action_turn_on, target_second=target_second, target_minute=target_minute, target_hour=target_hour, target_day=target_day, target_month=target_month, target_year=target_year, original_timer_length_in_seconds=original_timer_length_in_seconds)

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

        raise Exception('Unsupported message')
