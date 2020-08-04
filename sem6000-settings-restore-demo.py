#!/usr/bin/python3

import datetime
import json
import sys

import sem6000
from message import *


def _format_minutes_as_time(minutes):
    hour = minutes // 60
    minute = minutes - hour*60

    return "{:02}:{:02}".format(hour, minute)

def _format_seconds_as_time(seconds):
    hour = seconds // (60*60)
    seconds -= hour*60*60

    minute = seconds // 60
    seconds -= minute*60

    second = seconds

    return "{:02}:{:02}:{:02}".format(hour, minute, second)


if len(sys.argv) <= 1:
    print("Usage: " + sys.argv[0] + " <bluetooth address> <pin>", file=sys.stderr)
else:
    address = sys.argv[1]
    pin = sys.argv[2]
    json_file = sys.argv[3]

    f = open(json_file)
    data = json.load(f)
    f.close()

    device = sem6000.SEM6000(address, pin, debug=True)
    device.factory_reset()
    device.disconnect()

    device = sem6000.SEM6000(address, "0000", debug=True)
    device.change_pin(pin)

    device.set_date_and_time(datetime.datetime.now().isoformat())
    device.set_device_name(data["device-name"])

    device.set_prices(data["settings"]["normal-price-in-cent"], data["settings"]["reduced-period"]["price-in-cent"])
    device.set_reduced_period(data["settings"]["reduced-period"]["is-active"], _format_minutes_as_time(data["settings"]["reduced-period"]["start-time-in-minutes"]), _format_minutes_as_time(data["settings"]["reduced-period"]["end-time-in-minutes"]))

    if data["settings"]["is-led-active"]:
        device.led_on()
    else:
        device.led_off()

    device.set_power_limit(data["settings"]["power-limit-in-watt"])

    start_time = datetime.time(data["random-mode"]["start-hour"], data["random-mode"]["start-minute"])
    end_time = datetime.time(data["random-mode"]["end-hour"], data["random-mode"]["end-minute"])
    if data["random-mode"]["is-active"]:
        device.set_random_mode(data["random-mode"]["active-on-weekdays"], start_time.isoformat(), end_time.isoformat())
    else:
        device.reset_random_mode()

    slot_ids = list(data["scheduler"]["entries"].keys())
    slot_ids.reverse()
    for slot_id in slot_ids:
        scheduler = data["scheduler"]["entries"][slot_id]

        target_datetime = datetime.datetime(scheduler["year"], scheduler["month"], scheduler["day"], scheduler["hour"], scheduler["minute"])

        device.add_scheduler(scheduler["is-active"], scheduler["is-action-turn-on"], scheduler["repeat-on-weekdays"], target_datetime.isoformat())

