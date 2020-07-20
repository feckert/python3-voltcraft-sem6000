#!/usr/bin/python3

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


def _format_minutes_as_time(minutes):
    hour = minutes // 60
    minute = minutes - hour*60

    return "{:02}:{:02}".format(hour, minute)


def _format_hour_and_minute_as_time(hour, minute):
    return "{:02}:{:02}".format(hour, minute)


def _parse_boolean(boolean_string):
    boolean_value = False

    if str(boolean_string).lower() == "true":
        boolean_value = True
    if str(boolean_string).lower() == "on":
        boolean_value = True
    if str(boolean_string).lower() == "1":
        boolean_value = True

    return boolean_value


if __name__ == '__main__':
    if len(sys.argv) == 1:
        devices = SEM6000.discover()
        for device in devices:
            print(device['name'] + '\t' + device['address'])
    else:
        deviceAddr = sys.argv[1]
        pin = sys.argv[2]
        cmd = sys.argv[3]

        sem6000 = SEM6000(deviceAddr, pin, debug=True)

        if cmd != 'reset_pin':
            sem6000.authorize()

        if cmd == 'change_pin':
            sem6000.change_pin(sys.argv[4])
        if cmd == 'reset_pin':
            sem6000.reset_pin()
        if cmd == 'power_on':
            sem6000.power_on()
        if cmd == 'power_off':
            sem6000.power_off()
        if cmd == 'led_on':
            sem6000.led_on()
        if cmd == 'led_off':
            sem6000.led_off()
        if cmd == 'set_date_and_time':
            sem6000.set_date_and_time(sys.argv[4])
        if cmd == 'synchronize_date_and_time':
            sem6000.set_date_and_time(datetime.datetime.now().isoformat())
        if cmd == 'request_settings':
            response = sem6000.request_settings()
            assert isinstance(response, RequestedSettingsNotification)

            print("Settings:")
            if response.is_reduced_mode_active:
                print("\tReduced mode:\t\tOn")
            else:
                print("\tReduced mode:\t\tOff")

            print("\tNormal price:\t\t{:.2f} EUR".format(response.normal_price_in_cent/100))
            print("\tReduced price:\t\t{:.2f} EUR".format(response.reduced_price_in_cent/100))

            print("\tRecuced mode start:\t{} minutes ({})".format(response.reduced_mode_start_time_in_minutes, _format_minutes_as_time(response.reduced_mode_start_time_in_minutes)))
            print("\tRecuced mode end:\t{} minutes ({})".format(response.reduced_mode_end_time_in_minutes, _format_minutes_as_time(response.reduced_mode_end_time_in_minutes)))

            if response.is_led_active:
                print("\tLED state;\t\tOn")
            else:
                print("\tLED state;\t\tOff")

            print("\tPower limit:\t\t{} W".format(response.power_limit_in_watt))
        if cmd == 'set_power_limit':
            sem6000.set_power_limit(power_limit_in_watt=sys.argv[4])
        if cmd == 'set_prices':
            sem6000.set_prices(normal_price_in_cent=sys.argv[4], reduced_price_in_cent=sys.argv[5])
        if cmd == 'set_reduced_period':
            sem6000.set_reduced_period(is_active=sys.argv[4], start_isotime=sys.argv[5], end_isotime=sys.argv[6])
        if cmd == 'request_timer_status':
            response = sem6000.request_timer_status()
            assert isinstance(response, RequestedTimerStatusNotification)

            original_timer_length = datetime.timedelta(seconds=response.original_timer_length_in_seconds)

            print("Timer Status:")
            if response.is_timer_running:
                now = datetime.datetime.now()
                now = datetime.datetime(now.year % 100, now.month, now.day, now.hour, now.minute, now.second)

                dt = datetime.datetime(response.target_year, response.target_month, response.target_day, response.target_hour, response.target_minute, response.target_second)
                time_left = (dt - now)

                print("\tTimer state:\t\tOn")
                print("\tTime left:\t\t" + str(time_left))
                if response.is_action_turn_on:
                    print("\tAction:\t\t\tTurn On")
                else:
                    print("\tAction:\t\t\tTurn Off")
            else:
                print("\tTimer state:\t\tOff")

            print("\tOriginal timer length:\t" + str(original_timer_length))
        if cmd == 'set_timer':
            sem6000.set_timer(False, sys.argv[4], sys.argv[5])
        if cmd == 'reset_timer':
            sem6000.set_timer(True, False, "00:00")
        if cmd == 'request_scheduler':
            response = sem6000.request_scheduler()

            print("Schedulers:")
            for i in range(len(response.schedulers)):
                scheduler = response.schedulers[i]

                print("\t#" + str(i+1))
                
                if scheduler.is_active:
                    print("\tActive:\tOn")
                else:
                    print("\tActive:\tOff")

                if scheduler.is_action_turn_on:
                    print("\tAction:\tTurn On")
                else:
                    print("\tAction:\tTurn Off")
                
                if scheduler.repeat_on_weekdays:
                    repeat_on_weekdays = ""
                    is_first_value = True
                    for weekday in scheduler.repeat_on_weekdays:
                        if not is_first_value:
                            repeat_on_weekdays += ", "
                        repeat_on_weekdays += weekday.name
                        is_first_value = False

                    print("\tRepeat on:\t" + repeat_on_weekdays)
                else:
                    date = datetime.date(year=scheduler.year, month=scheduler.month, day=scheduler.day)
                    print("\tDate:\t" + str(date))

                print("\tTime:\t" + _format_hour_and_minute_as_time(scheduler.hour, scheduler.minute))
                print("")

