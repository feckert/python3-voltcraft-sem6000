#!/usr/bin/python3

import sys

from sem6000 import sem6000
from sem6000.message import *

if len(sys.argv) <= 1:
    print("Usage: " + sys.argv[0] + " <bluetooth address> <pin>", file=sys.stderr)
else:
    address = sys.argv[1]
    pin = sys.argv[2]

    device = sem6000.SEM6000(address, pin, debug=True)

    consumption_of_last_12_months_response = device.request_consumption_of_last_12_months()
    assert len(consumption_of_last_12_months_response.consumption_n_months_ago_in_watt_hour) == 1+12

    consumption_of_last_30_days_response = device.request_consumption_of_last_30_days()
    assert len(consumption_of_last_30_days_response.consumption_n_days_ago_in_watt_hour) == 1+30

    consumption_of_last_23_days_response = device.request_consumption_of_last_23_hours()
    assert len(consumption_of_last_23_days_response.consumption_n_hours_ago_in_watt_hour) == 1+23

    measurement_response = device.request_measurement()
    assert measurement_response.power_in_milliwatt > 0
    assert measurement_response.current_in_milliampere > 0
    assert measurement_response.voltage_in_volt > 0
    assert measurement_response.frequency_in_hertz > 0
    assert measurement_response.is_power_active

    timer_status_response = device.request_timer_status()
    assert not timer_status_response.is_timer_running

    device_serial_response = device.request_device_serial()
    assert len(device_serial_response.serial) > 0


