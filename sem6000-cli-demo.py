#!/usr/bin/python3

import sem6000
from message import *
from message import _format_list_of_objects

import datetime
import sys

def _format_minutes_as_time(minutes):
    hour = minutes // 60
    minute = minutes - hour*60

    return "{:02}:{:02}".format(hour, minute)


def _format_hour_and_minute_as_time(hour, minute):
    return "{:02}:{:02}".format(hour, minute)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        devices = sem6000.SEM6000.discover()
        for device in devices:
            print(device['name'] + '\t' + device['address'])
    else:
        deviceAddr = sys.argv[1]
        pin = sys.argv[2]
        cmd = sys.argv[3]

        sem6000 = sem6000.SEM6000(deviceAddr, debug=True)

        if cmd != 'reset_pin' and cmd != 'get_device_name':
            sem6000.authorize(pin)

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
            for i in range(len(response.scheduler_entries)):
                scheduler_entry = response.scheduler_entries[i]
                scheduler = scheduler_entry.scheduler

                print("\t#" + str(scheduler_entry.slot_id))

                if scheduler.is_active:
                    print("\tActive:\t\t\tOn")
                else:
                    print("\tActive:\t\t\tOff")

                if scheduler.is_action_turn_on:
                    print("\tAction:\t\t\tTurn On")
                else:
                    print("\tAction:\t\t\tTurn Off")

                if scheduler.repeat_on_weekdays:
                    weekday_formatter = lambda w: w.name
                    repeat_on_weekdays = _format_list_of_objects(weekday_formatter, scheduler.repeat_on_weekdays)
                    print("\tRepeat on weekdays:\t" + repeat_on_weekdays)
                else:
                    date = datetime.date(year=scheduler.year, month=scheduler.month, day=scheduler.day)
                    print("\tDate:\t\t\t" + str(date))

                print("\tTime:\t\t\t" + _format_hour_and_minute_as_time(scheduler.hour, scheduler.minute))
                print("")
        if cmd == 'add_scheduler':
            is_active = sys.argv[4]
            is_action_turn_on = sys.argv[5]
            repeat_on_weekdays=sys.argv[6]
            isodatetime = sys.argv[7]

            response = sem6000.add_scheduler(is_active=is_active, is_action_turn_on=is_action_turn_on, repeat_on_weekdays=repeat_on_weekdays, isodatetime=isodatetime)
        if cmd == 'edit_scheduler':
            slot_id = sys.argv[4]
            is_active = sys.argv[5]
            is_action_turn_on = sys.argv[6]
            repeat_on_weekdays=sys.argv[7]
            isodatetime = sys.argv[8]

            response = sem6000.edit_scheduler(slot_id=slot_id, is_active=is_active, is_action_turn_on=is_action_turn_on, repeat_on_weekdays=repeat_on_weekdays, isodatetime=isodatetime)
        if cmd == 'remove_scheduler':
            slot_id = sys.argv[4]

            response = sem6000.remove_scheduler(slot_id=slot_id)
        if cmd == 'request_random_mode_status':
            response = sem6000.request_random_mode_status()

            if response.is_active:
                print("\tActive:\t\t\tOn")
            else:
                print("\tActive:\t\t\tOff")

            weekday_formatter = lambda w: w.name
            active_on_weekdays = _format_list_of_objects(weekday_formatter, response.active_on_weekdays)
            print("\tActive on weekdays:\t" + active_on_weekdays)
            print("")
        if cmd == 'set_random_mode':
            is_active = sys.argv[4]
            active_on_weekdays = sys.argv[5]
            start_hour = sys.argv[6]
            start_minute = sys.argv[7]
            end_hour = sys.argv[8]
            end_minute = sys.argv[9]

            response = sem6000.set_random_mode(is_active=is_active, active_on_weekdays=active_on_weekdays, start_hour=start_hour, start_minute=start_minute, end_hour=end_hour, end_minute=end_minute)
        if cmd == 'request_device_name':
            device_name = sem6000.request_device_name()

            print("Device-Name:\t" + device_name)
        if cmd == 'set_device_name':
            new_name = sys.argv[4]

            sem6000.set_device_name(new_name=new_name)
        if cmd == 'request_device_serial':
            response = sem6000.request_device_serial()

            print("Device-Serial:\t" + str(response.serial))
