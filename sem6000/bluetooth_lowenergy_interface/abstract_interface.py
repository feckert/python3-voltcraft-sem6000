from abc import *

class AbstractBluetoothInterface(ABC):
    def __init__(self, mac_address=None, bluetooth_device='hci0'):
        self.mac_addess = mac_address
        self.bluetooth_device = bluetooth_device

        self._is_notifications_enabled = False
        self._notification_handler = []

    def enable_notifications(self):
        '''Enables reception of notifications from the device'''

        self._is_notifications_enabled = True

    def disable_notifications(self):
        '''Disables reception of notifications from the device'''

        self._is_notifications_enabled = False

    @abstractmethod
    def discover(self, timeout, service_uuids=[]):
        '''
        Returns a list of discovered devices.

        Parameters:
            timeout (int):              Maximum amount of seconds to wait for device advertisements
            service_uuds (list of str): When given only devices advertising one of these services are returned

        Returns:
            A list of dictionaries having keys 'address' and 'name'
        '''

        pass

    @abstractmethod
    def connect(self, mac_address):
        '''Connects to the given device'''

        pass

    @abstractmethod
    def disconnect(self):
        '''Disconnects from the currently connected device'''

        pass

    @abstractmethod
    def is_connected(self):
        '''Returns True if connected to a device'''

        pass

    @abstractmethod
    def write_to_characteristic(self, uuid, data):
        '''
        Send data to the characteristics identified by uuid of the currently connected device

        Parameters:
            uuid (str):     UUID of the form 00000000-0000-0000-0000-000000000000
            data (bytes):   data to send 
        '''

        pass

    @abstractmethod
    def read_from_characteristic(self, uuid):
        '''
        Read data from the characteristics identified by uuid

        Parameters:
            uuid (str):     UUID of the form 00000000-0000-0000-0000-000000000000
        '''

        pass

    @abstractmethod
    def wait_for_notifications(self, timeout):
        '''
        Waits for notifications

        Parameters:
            timeout (int):  Maximum amount of seconds to wait for incoming notifications

        Returns:
            True if a notification was received
            False if no notification was received
        '''

        pass

    def add_notification_handler(self, notification_handler):
        '''
        Registers a callable object to handle incoming notifications

        Parameters:
            notification_handler (callable):    Callable object which is being called with (characteristic_uuid, data) when a notification was received
        '''

        self._notification_handler.append(notification_handler)

    def _send_notification_to_handlers(self, characteristic_uuid, data):
        for handler in self._notification_handler:
            handler(characteristic_uuid, data)

