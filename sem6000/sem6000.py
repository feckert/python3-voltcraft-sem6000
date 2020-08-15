import binascii
import datetime
import sys

from .bluetooth_lowenergy_interface.bluepy_interface import *
from . import encoder
from .message import *
from . import parser
from . import util


class SEM6000Delegate():
    def __init__(self, debug=False):
        btle.DefaultDelegate.__init__(self)

        self.debug = False
        if debug:
            self.debug = True

        self._raw_notifications = []

        self._parser = parser.MessageParser()

    def __call__(self, characteristic_uuid, data):
        self._handle_notification(characteristic_uuid, data)

    def _handle_notification(self, characteristic_uuid, data):
        self._raw_notifications.append(data)

    def has_final_raw_notification(self):
        if len(self._raw_notifications) == 0:
            return False

        last_notification = self._raw_notifications[-1]

        if len(last_notification) < 2:
            return False

        # command b'\x04\x00' lacks suffix b'\xff\xff'
        if last_notification[2:4] == b'\x04\x00':
            return True

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

    def reset_notification_data(self):
        self._raw_notifications.clear()


class SEM6000():
    SERVICECLASS_UUID='0000fff0-0000-1000-8000-00805f9b34fb'
    CHARACTERISTIC_UUID_NAME='00002a00-0000-1000-8000-00805f9b34fb'
    CHARACTERISTIC_UUID_CONTROL='0000fff3-0000-1000-8000-00805f9b34fb'
    CHARACTERISTIC_UUID_RESPONSE='0000fff4-0000-1000-8000-00805f9b34fb'

    def __init__(self, deviceAddr=None, pin=None, bluetooth_device='hci0', timeout=3, debug=False):
        self.timeout = timeout
        self.debug = debug

        self.connection_settings = {}

        self.pin = None

        self._encoder = encoder.MessageEncoder()

        self._delegate = SEM6000Delegate(self.debug)
        self._bluetooth_lowenergy_interface = BluePyBtLeInterface(bluetooth_device=bluetooth_device)
        self._bluetooth_lowenergy_interface.add_notification_handler(self._delegate._handle_notification)

        if not deviceAddr is None:
            self.connect(deviceAddr)

        if not pin is None:
            self.authorize(pin)

    def _disconnect(self):
        if self._bluetooth_lowenergy_interface:
            self._bluetooth_lowenergy_interface.disconnect()

            return True

        return False

    def _reconnect(self):
        self._disconnect()

        try:
            self._bluetooth_lowenergy_interface.connect(self.connection_settings["deviceAddr"])
        except btle.BTLEException as e:
            self._disconnect()
            raise e

        self._bluetooth_lowenergy_interface.enable_notifications()

        if self.pin:
            try:
                self.authorize(self.pin)
            except Exception as e:
                self._disconnect()
                raise e

    def _is_connected(self):
        if self._bluetooth_lowenergy_interface is None:
            return False

        return self._bluetooth_lowenergy_interface.is_connected()

    def _send_command(self, command):
        encoded_command = self._encoder.encode(command)

        if self.debug:
            print("sent data: " + str(binascii.hexlify(encoded_command)) + " (" + str(command) + ")", file=sys.stderr)

        self._delegate.reset_notification_data()

        if not self._is_connected():
            if self.connection_settings["deviceAddr"] and self.pin:
                self._reconnect()
            else:
                raise Exception("Not connected and no deviceAddress / pin set")

        self._bluetooth_lowenergy_interface.write_to_characteristic(SEM6000.CHARACTERISTIC_UUID_CONTROL, encoded_command)
        self._wait_for_notifications()

    def _wait_for_notifications(self):
        while True:
            if not self._bluetooth_lowenergy_interface.wait_for_notifications(self.timeout):
                break

            if self._delegate.has_final_raw_notification():
                break

    def _consume_notification(self):
        return self._delegate.consume_notification()

    def connect(self, deviceAddr):
        self.connection_settings["deviceAddr"] = deviceAddr

        return self._reconnect()

    def disconnect(self):
        return self._disconnect()

    def discover(timeout=5, bluetooth_device='hci0'):
        bluetooth_lowenergy_interface = BluePyBtLeInterface(bluetooth_device=bluetooth_device)

        return bluetooth_lowenergy_interface.discover(timeout, service_uuids=[SEM6000.SERVICECLASS_UUID])

    def request_device_name(self):
        data = self._bluetooth_lowenergy_interface.read_from_characteristic(SEM6000.CHARACTERISTIC_UUID_NAME)

        if self.debug:
            print("received data: " + str(binascii.hexlify(data)), file=sys.stderr)

        return data.decode(encoding='utf-8')

    def authorize(self, pin):
        command = AuthorizeCommand(pin)
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, AuthorizationNotification):
            raise Exception("Authentication failed")

        if notification.was_successful:
            self.pin = pin
        else:
            self.pin = None
            raise Exception("Authentication failed")

        return notification

    def change_pin(self, new_pin):
        command = ChangePinCommand(self.pin, new_pin)
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, ChangePinNotification) or not notification.was_successful:
            raise Exception("Change PIN failed")

        return notification

    def reset_pin(self):
        command = ResetPinCommand()
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, ResetPinNotification) or not notification.was_successful:
            raise Exception("Reset PIN failed")

        return notification

    def power_on(self):
        command = PowerSwitchCommand(True)
        self._send_command(command)
        notification = self._consume_notification()
        
        if not isinstance(notification, PowerSwitchNotification) or not notification.was_successful:
            raise Exception("Power on failed")

        return notification

    def power_off(self):
        command = PowerSwitchCommand(False)
        self._send_command(command)
        notification = self._consume_notification()
        
        if not isinstance(notification, PowerSwitchNotification) or not notification.was_successful:
            raise Exception("Power off failed")

        return notification

    def led_on(self):
        command = LEDSwitchCommand(True)
        self._send_command(command)
        notification = self._consume_notification()
        
        if not isinstance(notification, LEDSwitchNotification) or not notification.was_successful:
            raise Exception("LED on failed")

        return notification

    def led_off(self):
        command = LEDSwitchCommand(False)
        self._send_command(command)
        notification = self._consume_notification()
        
        if not isinstance(notification, LEDSwitchNotification) or not notification.was_successful:
            raise Exception("LED off failed")

        return notification

    def set_date_and_time(self, isodatetime):

        command = SynchronizeDateAndTimeCommand(isodatetime)
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, SynchronizeDateAndTimeNotification) or not notification.was_successful:
            raise Exception("Set date and time failed")

        return notification

    def request_settings(self):
        command = RequestSettingsCommand()
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, RequestedSettingsNotification):
            raise Exception("Request settings failed")

        return notification

    def set_power_limit(self, power_limit_in_watt):
        command = SetPowerLimitCommand(power_limit_in_watt=int(power_limit_in_watt))
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, PowerLimitSetNotification) or not notification.was_successful:
            raise Exception("Set power limit failed")

        return notification

    def set_prices(self, normal_price_in_cent, reduced_period_price_in_cent):
        command = SetPricesCommand(normal_price_in_cent=int(normal_price_in_cent), reduced_period_price_in_cent=int(reduced_period_price_in_cent))
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, PricesSetNotification) or not notification.was_successful:
            raise Exception("Set prices failed")

        return notification

    def set_reduced_period(self, is_active, start_isotime, end_isotime):
        command = SetReducedPeriodCommand(is_active=util._parse_boolean(is_active), start_isotime=start_isotime, end_isotime=end_isotime)
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, ReducedPeriodSetNotification) or not notification.was_successful:
            raise Exception("Set reduced period failed")

        return notification

    def request_timer_status(self):
        command = RequestTimerStatusCommand()
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, RequestedTimerStatusNotification):
            raise Exception("Request timer status failed")

        return notification

    def set_timer(self, is_action_turn_on, delay_isotime):
        time = datetime.time.fromisoformat(delay_isotime)
        timedelta = datetime.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
        dt = datetime.datetime.now() + timedelta

        command = SetTimerCommand(is_reset_timer=False, is_action_turn_on=util._parse_boolean(is_action_turn_on), target_isodatetime=dt.isoformat(timespec='seconds'))
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, TimerSetNotification) or not notification.was_successful:
            raise Exception("Set timer failed")

        return notification

    def reset_timer(self):
        command = SetTimerCommand(is_reset_timer=True, is_action_turn_on=False)
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, TimerSetNotification) or not notification.was_successful:
            raise Exception("Reset timer failed")

        return notification

    def request_scheduler(self):
        command = RequestSchedulerCommand(page_number=0)
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, SchedulerRequestedNotification):
            raise Exception('Request scheduler 1st page failed')

        max_page_number = notification.number_of_schedulers // 4
        for page_number in range(1, max_page_number+1):
            command = RequestSchedulerCommand(page_number=page_number)
            self._send_command(command)
            further_notification = self._consume_notification()

            if not isinstance(further_notification, SchedulerRequestedNotification):
                raise Exception('Request scheduler 2nd page failed')

            notification.scheduler_entries.extend(further_notification.scheduler_entries)

        return notification

    def add_scheduler(self, is_active, is_action_turn_on, repeat_on_weekdays, isodatetime):
        command = AddSchedulerCommand(Scheduler(is_active=util._parse_boolean(is_active), is_action_turn_on=util._parse_boolean(is_action_turn_on), repeat_on_weekdays=util._parse_weekdays_list(repeat_on_weekdays), isodatetime=isodatetime))
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, SchedulerSetNotification) or not notification.was_successful:
            raise Exception("Add scheduler failed")

        return notification

    def edit_scheduler(self, slot_id, is_active, is_action_turn_on, repeat_on_weekdays, isodatetime):
        command = EditSchedulerCommand(slot_id=int(slot_id), scheduler=Scheduler(is_active=util._parse_boolean(is_active), is_action_turn_on=util._parse_boolean(is_action_turn_on), repeat_on_weekdays=tuil._parse_weekdays_list(repeat_on_weekdays), isodatetime=isodatetime))
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, SchedulerSetNotification) or not notification.was_successful:
            raise Exception("Edit scheduler failed")

        return notification

    def remove_scheduler(self, slot_id):
        command = RemoveSchedulerCommand(slot_id=int(slot_id))
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, SchedulerSetNotification) or not notification.was_successful:
            raise Exception("Remove scheduler failed")

        return notification

    def request_random_mode_status(self):
        command = RequestRandomModeStatusCommand()
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, RandomModeStatusRequestedNotification):
            raise Exception("Request random mode status failed")

        return notification

    def set_random_mode(self, active_on_weekdays, start_isotime, end_isotime):
        command = SetRandomModeCommand(is_active=True, active_on_weekdays=util._parse_weekdays_list(active_on_weekdays), start_isotime=start_isotime, end_isotime=end_isotime)
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, RandomModeSetNotification) or not notification.was_successful:
            raise Exception("Set random mode failed")

        return notification

    def reset_random_mode(self):
        command = SetRandomModeCommand(is_active=False, active_on_weekdays=[], start_isotime="00:00", end_isotime="00:00")
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, RandomModeSetNotification) or not notification.was_successful:
            raise Exception("Set random mode failed")

        return notification

    def request_measurement(self):
        command = RequestMeasurementCommand()
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, MeasurementRequestedNotification):
            raise Exception("Request measurement failed")

        return notification

    def request_consumption_of_last_12_months(self):
        command = RequestConsumptionOfLast12MonthsCommand()
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, ConsumptionOfLast12MonthsRequestedNotification):
            raise("Request consumption of last 12 months failed")

        return notification

    def request_consumption_of_last_30_days(self):
        command = RequestConsumptionOfLast30DaysCommand()
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, ConsumptionOfLast30DaysRequestedNotification):
            raise("Request consumption of last 30 days failed")

        return notification

    def request_consumption_of_last_23_hours(self):
        command = RequestConsumptionOfLast23HoursCommand()
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, ConsumptionOfLast23HoursRequestedNotification):
            raise("Request consumption of last 23 hours failed")

        return notification

    def reset_consumption(self):
        command = ResetConsumptionCommand()
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, ResetConsumptionNotification) or not notification.was_successful:
            raise("Reset consumption failed")

        return notification

    def factory_reset(self):
        command = FactoryResetCommand()
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, FactoryResetNotification) or not notification.was_successful:
            raise("Factory reset failed")

        return notification

    def set_device_name(self, new_name):
        command = SetDeviceNameCommand(new_name=new_name)
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, DeviceNameSetNotification) or not notification.was_successful:
            raise Exception("Set device name failed")

        return notification

    def request_device_serial(self):
        command = RequestDeviceSerialCommand()
        self._send_command(command)
        notification = self._consume_notification()

        if not isinstance(notification, DeviceSerialRequestedNotification):
            raise Exception("Request device serial failed")

        return notification
