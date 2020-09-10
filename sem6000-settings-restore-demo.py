#!/usr/bin/python3

import datetime
import json
import sys

from sem6000 import sem6000
from sem6000.message import *


if len(sys.argv) <= 1:
    print("Usage: " + sys.argv[0] + " <bluetooth address> <pin> <settings backup file>", file=sys.stderr)
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

    device.change_device_name(data["device-name"])

    device.change_prices(data["settings"]["normal-price-in-cent"], data["settings"]["reduced-period"]["price-in-cent"])
    device.change_reduced_period(data["settings"]["reduced-period"]["is-active"], data["settings"]["reduced-period"]["start-isotime"], data["settings"]["reduced-period"]["end-isotime"])

    if data["settings"]["is-nightmode-active"]:
        device.nightmode_on()
    else:
        device.nightmode_off()

    device.change_power_limit(data["settings"]["power-limit-in-watt"])

    if data["random-mode"]["is-active"]:
        device.change_random_mode(data["random-mode"]["active-on-weekdays"], data["random-mode"]["start-isotime"], data["random-mode"]["end-isotime"])
    else:
        device.reset_random_mode()

    if data["timer"]["is-active"]:
        device.activate_timer_at(data["timer"]["is-action-turn-on"], data["timer"]["isodatetime"])

    slot_ids = list(data["scheduler"]["entries"].keys())
    slot_ids.reverse()
    for slot_id in slot_ids:
        scheduler = data["scheduler"]["entries"][slot_id]

        if not "repeat-on-weekdays" in scheduler:
            device.add_onetime_scheduler(scheduler["is-active"], scheduler["is-action-turn-on"], scheduler["isodatetime"])
        else:
            device.add_repeated_scheduler(scheduler["is-active"], scheduler["is-action-turn-on"], scheduler["repeat-on-weekdays"], scheduler["isotime"])
