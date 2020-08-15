from abc import *

class AbstractBluetoothInterface(ABC):
    def __init__(self, mac_address=None, bluetooth_device='hci0'):
        self.mac_addess = mac_address
        self.bluetooth_device = bluetooth_device

        self._is_notifications_enabled = False
        self._notification_handler = []

    def enable_notifications(self):
        self._is_notifications_enabled = True

    def disable_notifications(self):
        self._is_notifications_enabled = False

    @abstractmethod
    def discover(self, timeout, service_uuids=[]):
        pass

    @abstractmethod
    def connect(self, mac_address):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def is_connected(self):
        pass

    @abstractmethod
    def write_to_characteristic(self, uuid, data):
        pass

    @abstractmethod
    def read_from_characteristic(self, uuid):
        pass

    @abstractmethod
    def wait_for_notifications(self, timeout):
        pass

    def add_notification_handler(self, notification_handler):
        self._notification_handler.append(notification_handler)

    def _send_notification_to_handlers(self, characteristic_uuid, data):
        for handler in self._notification_handler:
            handler(characteristic_uuid, data)

