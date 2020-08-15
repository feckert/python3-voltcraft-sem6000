from . import abstract_interface

from bluepy import btle

import sys

class BluePyBtLeDelegate(btle.DefaultDelegate):
    def __init__(self, bluepy_bluetooth_interface):
        btle.DefaultDelegate.__init__(self)

        self._bluepy_bluetooth_interface = bluepy_bluetooth_interface

    def handleNotification(self, cHandle, data):
        self._bluepy_bluetooth_interface._handle_notification(cHandle, data)


class BluePyBtLeInterface(abstract_interface.AbstractBluetoothInterface):
    def __init__(self, mac_address=None, bluetooth_device='hci0'):
        abstract_interface.AbstractBluetoothInterface.__init__(self, mac_address, bluetooth_device)

        self._peripheral = None
        self._delegate = BluePyBtLeDelegate(self)

        self._characteristic_by_uuid = {}
        self._characteristic_by_bluepy_handle = {}

    def _get_characteristic(self, uuid):
        if uuid in self._characteristic_by_uuid:
            characteristic = self._characteristic_by_uuid[uuid]
        else:
            characteristic = self._peripheral.getCharacteristics(uuid=uuid)[0]

            self._characteristic_by_uuid[str(characteristic.uuid)] = characteristic
            self._characteristic_by_bluepy_handle[characteristic.valHandle] = characteristic

        return characteristic

    def _get_characteristic_by_bluepy_handle(self, bluepy_handle):
        if bluepy_handle in self._characteristic_by_bluepy_handle:
            characteristic = self._characteristic_by_bluepy_handle[bluepy_handle]
        else:
            characteristics = self._peripheral.getCharacteristics()

            characteristic = None
            for c in characteristics:
                if c.valHandle == bluepy_handle:
                    characteristic = c
                    break

            self._characteristic_by_uuid[str(characteristic.uuid)] = characteristic
            self._characteristic_by_bluepy_handle[characteristic.valHandle] = characteristic

        return characteristic

    def _handle_notification(self, characteristic_bluepy_handle, data):
        characteristic = self._get_characteristic_by_bluepy_handle(characteristic_bluepy_handle)
        uuid = str(characteristic.uuid)

        self._send_notification_to_handlers(uuid, data)

    def discover(self, timeout, service_uuids=[]):
        result = []

        scanner = btle.Scanner()
        scanner_results = scanner.scan(timeout)

        for device in scanner_results:
            address = device.addr

            scanned_incomplete_16b_service_uuids = device.getValueText(btle.ScanEntry.INCOMPLETE_16B_SERVICES)
            scanned_complete_16b_service_uuids = device.getValueText(btle.ScanEntry.COMPLETE_16B_SERVICES)

            scanned_incomplete_32b_service_uuids = device.getValueText(btle.ScanEntry.INCOMPLETE_32B_SERVICES)
            scanned_complete_32b_service_uuids = device.getValueText(btle.ScanEntry.COMPLETE_32B_SERVICES)

            scanned_incomplete_128b_service_uuids = device.getValueText(btle.ScanEntry.INCOMPLETE_128B_SERVICES)
            scanned_complete_128b_service_uuids = device.getValueText(btle.ScanEntry.COMPLETE_128B_SERVICES)

            complete_local_name = device.getValueText(btle.ScanEntry.COMPLETE_LOCAL_NAME)

            if len(service_uuids) > 0:
                is_services_matching = False
                for uuid in service_uuids:
                    if not scanned_incomplete_16b_service_uuids is None and uuid in scanned_incomplete_16b_service_uuids:
                        is_services_matching = True
                    if not scanned_complete_16b_service_uuids is None and uuid in scanned_complete_16b_service_uuids:
                        is_services_matching = True

                    if not scanned_incomplete_32b_service_uuids is None and uuid in scanned_incomplete_32b_service_uuids:
                        is_services_matching = True
                    if not scanned_complete_32b_service_uuids is None and uuid in scanned_complete_32b_service_uuids:
                        is_services_matching = True

                    if not scanned_incomplete_128b_service_uuids is None and uuid in scanned_incomplete_128b_service_uuids:
                        is_services_matching = True
                    if not scanned_complete_128b_service_uuids is None and uuid in scanned_complete_128b_service_uuids:
                        is_services_matching = True

                if not is_services_matching:
                    continue
                
            result.append({'address': address, 'name': complete_local_name})

        return result

    def connect(self, mac_address):
        self._peripheral = btle.Peripheral().withDelegate(self._delegate)
        try:
            iface = int(self.bluetooth_device.replace("hci", ""))
            self._peripheral.connect(mac_address, btle.ADDR_TYPE_PUBLIC, iface)
        except btle.BTLEException as e:
            self._peripheral = None
            raise e

    def disconnect(self):
        self._characteristic_by_uuid.clear()
        self._characteristic_by_bluepy_handle.clear()

        if self.is_connected():
            self._peripheral.disconnect()

    def is_connected(self):
        if self._peripheral is None:
            return False

        try:
            if self._peripheral.getState() != "conn":
                return False
        except btle.BTLEInternalError as e:
            return False

        return True

    def write_to_characteristic(self, uuid, data):
        characteristic = self._get_characteristic(uuid)

        return characteristic.write(data, self._is_notifications_enabled)

    def read_from_characteristic(self, uuid):
        characteristic = self._get_characteristic(uuid)

        return characteristic.read()

    def wait_for_notifications(self, timeout=None):
        if not timeout is None:
            return self._peripheral.waitForNotifications(timeout)
        else:
            return self._peripheral.waitForNotifications()

