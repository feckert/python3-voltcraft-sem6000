#!/usr/bin/python3

import json
import sys

from sem6000 import sem6000
from sem6000.message import *

if len(sys.argv) <= 1:
    print("Usage: " + sys.argv[0] + " <bluetooth address> <pin>", file=sys.stderr)
else:
    address = sys.argv[1]
    pin = sys.argv[2]

    device = sem6000.SEM6000(address, pin, debug=True)

    device_name_response = device.request_device_name()

    settings_response = device.request_settings()
    random_mode_response = device.request_random_mode_status()
    scheduler_response = device.request_scheduler()

    data = {}
    data["device-name"] = device_name_response.device_name

    data["settings"] = {
        "reduced-period": {
            "is-active": settings_response.is_reduced_period,
            "price-in-cent": settings_response.reduced_period_price_in_cent,
            "start-isotime": settings_response.reduced_period_start_isotime,
            "end-isotime": settings_response.reduced_period_end_isotime
        },
        "normal-price-in-cent": settings_response.normal_price_in_cent,
        "is-nightmode-active": settings_response.is_nightmode_active,
        "power-limit-in-watt": settings_response.power_limit_in_watt
    }

    weekdays = []
    for w in random_mode_response.active_on_weekdays:
        weekdays.append(w.value)

    data["random-mode"] = {
        "is-active": random_mode_response.is_active,
        "active-on-weekdays": weekdays,
        "start-isotime": random_mode_response.start_isotime,
        "end-isotime": random_mode_response.end_isotime
    }

    data["scheduler"] = {
        "number-of-schedulers": scheduler_response.number_of_schedulers,
        "entries": {
        }
    }

    d = data["scheduler"]["entries"]
    for entry in scheduler_response.scheduler_entries:
        scheduler = entry.scheduler
        weekdays = []
        for w in scheduler.repeat_on_weekdays:
            weekdays.append(w.value)

        dt = datetime.datetime.fromisoformat(scheduler.isodatetime)

        if not len(weekdays):
            d[entry.slot_id] = {
                "is-active": scheduler.is_active,
                "is-action-turn-on": scheduler.is_action_turn_on,
                "isodatetime": scheduler.isodatetime
            }
        else:
            d[entry.slot_id] = {
                "is-active": scheduler.is_active,
                "is-action-turn-on": scheduler.is_action_turn_on,
                "repeat-on-weekdays": weekdays,
                "isotime": dt.time().isoformat(timespec='minutes')
            }

    json.dump(data, sys.stdout, indent=True)
    print("")

