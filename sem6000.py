import binascii
import datetime
import sys
from bluepy import btle

import parser
import encoder
from message import *


class SEM6000Delegate(btle.DefaultDelegate):
    def __init__(self, debug=False):
        btle.DefaultDelegate.__init__(self)

        self.debug = False
        if debug:
            self.debug = True

        self._raw_notifications = []

        self._parser = parser.MessageParser()

    def handleNotification(self, cHandle, data):
        self._raw_notifications.append(data)

    def has_final_raw_notification(self):
        if len(self._raw_notifications) == 0:
            return False

        last_notification = self._raw_notifications[-1]

        if len(last_notification) < 2:
            return False

        return ( last_notification[-2:] == b'\xff\xff' )

    def consume_notification(self):
        exception = None
        notification = None

        data = b''
        for n in self._raw_notifications:
            data += n

        try:
            if not self.has_final_raw_notification():
                raise Exception("Incomplete notification data")

            notification = self._parser.parse(data)
        except Exception as e:
            if self.debug:
                print("received data: " + str(binascii.hexlify(data)) + " (Unknown Notification)", file=sys.stderr)
            raise e

        if self.debug:
            print("received data: " + str(binascii.hexlify(data)) + " (" + str(notification) + ")", file=sys.stderr)


        while len(self._raw_notifications):
            self._raw_notifications.pop(0)

        return notification


class SEM6000():
    def __init__(self, deviceAddr=None, pin=None, iface=None, debug=False):
        self.timeout = 10
        self.debug = debug

        self.pin = '0000'
        if not pin is None:
            self.pin = pin

        self._encoder = encoder.MessageEncoder()

        self._delegate = SEM6000Delegate(self.debug)
        self._peripheral = btle.Peripheral(deviceAddr=deviceAddr, addrType=btle.ADDR_TYPE_PUBLIC, iface=iface).withDelegate(self._delegate)
        self._characteristics = self._peripheral.getCharacteristics(uuid='0000fff3-0000-1000-8000-00805f9b34fb')[0]

    def _send_command(self, command):
        encoded_command = self._encoder.encode(command)

        if self.debug:
            print("sent data: " + str(binascii.hexlify(encoded_command)) + " (" + str(command) + ")", file=sys.stderr)

        self._characteristics.write(encoded_command)
        self._wait_for_notifications()

    def _wait_for_notifications(self):
        while True:
            if not self._peripheral.waitForNotifications(self.timeout):
                break

            if self._delegate.has_final_raw_notification():
                break 

    def discover(timeout=10):
        result = []

        scanner = btle.Scanner()
        scanner_results = scanner.scan(timeout)
        
        for device in scanner_results:
            address = device.addr
            # 0x02 - query "Incomplete List of 16-bit Service Class UUIDs"
            service_class_uuids = device.getValueText(2)
            # 0x09 - query complete local name
            complete_local_name = device.getValueText(9)

            if not service_class_uuids == "0000fff0-0000-1000-8000-00805f9b34fb":
                # not a sem6000 device
                continue

            result.append({'address': address, 'name': complete_local_name})

        return result

    def authorize(self):
        command = AuthorizeCommand(self.pin)
        self._send_command(command)
        notification = self._delegate.consume_notification()

        if not isinstance(notification, AuthorizationNotification) or not notification.was_successful:
            raise Exception("Authentication failed")

        return notification

    def change_pin(self, new_pin):
        command = ChangePinCommand(self.pin, new_pin)
        self._send_command(command)
        notification = self._delegate.consume_notification()

        if not isinstance(notification, ChangePinNotification) or not notification.was_successful:
            raise Exception("Change PIN failed")

        return notification

    def reset_pin(self):
        command = ResetPinCommand()
        self._send_command(command)
        notification = self._delegate.consume_notification()

        if not isinstance(notification, ResetPinNotification) or not notification.was_successful:
            raise Exception("Reset PIN failed")

        return notification

    def power_on(self):
        command = PowerSwitchCommand(True)
        self._send_command(command)
        notification = self._delegate.consume_notification()
        
        if not isinstance(notification, PowerSwitchNotification) or not notification.was_successful:
            raise Exception("Power on failed")

        return notification

    def power_off(self):
        command = PowerSwitchCommand(False)
        self._send_command(command)
        notification = self._delegate.consume_notification()
        
        if not isinstance(notification, PowerSwitchNotification) or not notification.was_successful:
            raise Exception("Power off failed")

        return notification

    def led_on(self):
        command = LEDSwitchCommand(True)
        self._send_command(command)
        notification = self._delegate.consume_notification()
        
        if not isinstance(notification, LEDSwitchNotification) or not notification.was_successful:
            raise Exception("LED on failed")

        return notification

    def led_off(self):
        command = LEDSwitchCommand(False)
        self._send_command(command)
        notification = self._delegate.consume_notification()
        
        if not isinstance(notification, LEDSwitchNotification) or not notification.was_successful:
            raise Exception("LED off failed")

        return notification

    def set_date_and_time(self, isodatetime):
        date_and_time = datetime.datetime.fromisoformat(isodatetime)

        command = SynchronizeDateAndTimeCommand(date_and_time.year, date_and_time.month, date_and_time.day, date_and_time.hour, date_and_time.minute, date_and_time.second)
        self._send_command(command)
        notification = self._delegate.consume_notification()

        if not isinstance(notification, SynchronizeDateAndTimeNotification) or not notification.was_successful:
            raise Exception("Set date and time failed")

        return notification

    def request_settings(self):
        command = RequestSettingsCommand()
        self._send_command(command)
        notification = self._delegate.consume_notification()

        if not isinstance(notification, RequestedSettingsNotification):
            raise Exception("Request settings failed")

        return notification

    def set_power_limit(self, power_limit_in_watt):
        command = SetPowerLimitCommand(power_limit_in_watt=int(power_limit_in_watt))
        self._send_command(command)
        notification = self._delegate.consume_notification()

        if not isinstance(notification, PowerLimitSetNotification):
            raise Exception("Set power limit failed")

        return notification

    def set_prices(self, normal_price_in_cent, reduced_price_in_cent):
        command = SetPricesCommand(normal_price_in_cent=int(normal_price_in_cent), reduced_price_in_cent=int(reduced_price_in_cent))
        self._send_command(command)
        notification = self._delegate.consume_notification()

        if not isinstance(notification, PricesSetNotification):
            raise Exception("Set prices failed")

        return notification

    def set_reduced_period(self, is_active, start_isotime, end_isotime):
        start_time = datetime.time.fromisoformat(start_isotime)
        end_time = datetime.time.fromisoformat(end_isotime)

        start_time_in_minutes = start_time.hour*60 + start_time.minute
        end_time_in_minutes = end_time.hour*60 + end_time.minute

        command = SetReducedPeriodCommand(is_active=_parse_boolean(is_active), start_time_in_minutes=start_time_in_minutes, end_time_in_minutes=end_time_in_minutes)
        self._send_command(command)
        notification = self._delegate.consume_notification()

        if not isinstance(notification, ReducedPeriodSetNotification):
            raise Exception("Set reduced period failed")

        return notification

    def request_timer_status(self):
        command = RequestTimerStatusCommand()
        self._send_command(command)
        notification = self._delegate.consume_notification()

        if not isinstance(notification, RequestedTimerStatusNotification):
            raise Exception("Request timer status failed")

        return notification

    def set_timer(self, is_reset_timer, is_action_turn_on, delay_isotime):
        time = datetime.time.fromisoformat(delay_isotime)
        timedelta = datetime.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
        dt = datetime.datetime.now() + timedelta
        dt = datetime.datetime(dt.year % 100, dt.month, dt.day, dt.hour, dt.minute, dt.second)

        command = SetTimerCommand(is_reset_timer=_parse_boolean(is_reset_timer), is_action_turn_on=_parse_boolean(is_action_turn_on), target_second=dt.second, target_minute=dt.minute, target_hour=dt.hour, target_day=dt.day, target_month=dt.month, target_year=dt.year)
        self._send_command(command)
        notification = self._delegate.consume_notification()

        if not isinstance(notification, TimerSetNotification):
            raise Exception("Set timer failed")

        return notification

    def request_scheduler(self):
        command = RequestSchedulerCommand(page_number=0)
        self._send_command(command)
        notification = self._delegate.consume_notification()

        if not isinstance(notification, SchedulerRequestedNotification):
            raise Exception('Request scheduler 1st page failed')

        max_page_number = notification.number_of_schedulers // 4
        for page_number in range(1, max_page_number+1):
            command = RequestSchedulerCommand(page_number=page_number)
            self._send_command(command)
            further_notification = self._delegate.consume_notification()

            if not isinstance(further_notification, SchedulerRequestedNotification):
                raise Exception('Request scheduler 2nd page failed')

            notification.schedulers.extend(further_notification.schedulers)

        return notification


