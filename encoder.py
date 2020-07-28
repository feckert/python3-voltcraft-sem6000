from message import *

class MessageEncoder():
    def _encode_message(self, payload, suffix=b'\xff\xff'):
        message = b'\x0f'

        message += (len(payload)+1).to_bytes(1, 'big')
        message += payload

        message += ((1+sum(payload)) & 0xff).to_bytes(1, 'big')
        message += suffix

        return message

    def _encode_pin(self, pin):
            pin_bytes = b''
            for i in pin:
                pin_bytes += int(i).to_bytes(1, 'big')
            
            return pin_bytes

    def _encode_scheduler(self, scheduler):
            is_active = b'\x00'
            if scheduler.is_active:
                is_active = b'\x01'

            is_action_turn_on = b'\x00'
            if scheduler.is_action_turn_on:
                is_action_turn_on = b'\x01'

            repeat_on_weekdays = 0
            for weekday in scheduler.repeat_on_weekdays:
                repeat_on_weekdays += 2**weekday.value
            repeat_on_weekdays = repeat_on_weekdays.to_bytes(1, 'big')

            year = scheduler.year.to_bytes(1, 'big')
            month = scheduler.month.to_bytes(1, 'big')
            day = scheduler.day.to_bytes(1, 'big')
            hour = scheduler.hour.to_bytes(1, 'big')
            minute = scheduler.minute.to_bytes(1, 'big')

            return is_active + is_action_turn_on + repeat_on_weekdays + year + month + day + hour + minute

    def encode(self, message):
        if isinstance(message, AuthorizeCommand):
            pin = self._encode_pin(message.pin)
            return self._encode_message(b'\x17\x00\x00' + pin + b'\x00\x00\x00\x00')

        if isinstance(message, ChangePinCommand):
            pin = self._encode_pin(message.pin)
            new_pin = self._encode_pin(message.new_pin)
            return self._encode_message(b'\x17\x00\x01' + new_pin + pin)

        if isinstance(message, ResetPinCommand):
            return self._encode_message(b'\x17\x00\x02' + b'\x00\x00\x00\x00\x00\x00\x00\x00')

        if isinstance(message, PowerSwitchCommand):
            if message.on:
                return self._encode_message(b'\x03\x00\x01' + b'\x00\x00')
            else:
                return self._encode_message(b'\x03\x00\x00' + b'\x00\x00')

        if isinstance(message, LEDSwitchCommand):
            if message.on:
                return self._encode_message(b'\x0f\x00\x05\x01' + b'\x00\x00\x00\x00')
            else:
                return self._encode_message(b'\x0f\x00\x05\x00' + b'\x00\x00\x00\x00')

        if isinstance(message, SynchronizeDateAndTimeCommand):
            year = message.year.to_bytes(2, 'big')
            month = message.month.to_bytes(1, 'big')
            day = message.day.to_bytes(1, 'big')

            hour = message.hour.to_bytes(1, 'big')
            minute = message.minute.to_bytes(1, 'big')
            second = message.second.to_bytes(1, 'big')

            return self._encode_message(b'\x01\x00' + second + minute + hour + day + month + year + b'\x00\x00')

        if isinstance(message, RequestSettingsCommand):
            return self._encode_message(b'\x10\x00' + b'\x00\x00')

        if isinstance(message, SetPowerLimitCommand):
            power_limit_in_watt = message.power_limit_in_watt.to_bytes(2, 'big')

            return self._encode_message(b'\x05\x00' + power_limit_in_watt + b'\x00\x00')

        if isinstance(message, SetPricesCommand):
            normal_price_in_cent = message.normal_price_in_cent.to_bytes(1, 'big')
            reduced_period_price_in_cent = message.reduced_period_price_in_cent.to_bytes(1, 'big')

            return self._encode_message(b'\x0f\x00\x04' + normal_price_in_cent + reduced_period_price_in_cent + b'\x00\x00\x00\x00')

        if isinstance(message, SetReducedPeriodCommand):
            is_active = b'\x00'
            if message.is_active:
                is_active = b'\x01'

            start_time_in_minutes = message.start_time_in_minutes.to_bytes(2, 'big')
            end_time_in_minutes = message.end_time_in_minutes.to_bytes(2, 'big')

            return self._encode_message(b'\x0f\x00\x01' + is_active + start_time_in_minutes + end_time_in_minutes)

        if isinstance(message, RequestTimerStatusCommand):
            return self._encode_message(b'\x09\x00\x00' + b'\x00')

        if isinstance(message, SetTimerCommand):
            timer_action = b'\x00'
            if not message.is_reset_timer:
                timer_action = b'\x02'
                if message.is_action_turn_on:
                    timer_action = b'\x01'

            target_second = message.target_second.to_bytes(1, 'big')
            target_minute = message.target_minute.to_bytes(1, 'big')
            target_hour = message.target_hour.to_bytes(1, 'big')
            target_day = message.target_day.to_bytes(1, 'big')
            target_month = message.target_month.to_bytes(1, 'big')
            target_year = message.target_year.to_bytes(1, 'big')

            return self._encode_message(b'\x08\x00' + timer_action + target_second + target_minute + target_hour + target_day + target_month + target_year + b'\x00\x00')

        if isinstance(message, RequestSchedulerCommand):
            page_number = message.page_number.to_bytes(1, 'big')

            return self._encode_message(b'\x14\x00' + page_number + b'\x00\x00')

        if isinstance(message, AddSchedulerCommand):
            return self._encode_message(b'\x13\x00' + b'\x00\x00' + self._encode_scheduler(message.scheduler) + b'\x00\x00')

        if isinstance(message, EditSchedulerCommand):
            slot_id = message.slot_id.to_bytes(1, 'big')

            return self._encode_message(b'\x13\x00' + b'\x01' + slot_id + self._encode_scheduler(message.scheduler) + b'\x00\x00')

        if isinstance(message, RemoveSchedulerCommand):
            slot_id = message.slot_id.to_bytes(1, 'big')

            return self._encode_message(b'\x13\x00' + b'\x02' + slot_id + b'\x00\x00\x00\x00\x00\x00\x00\x00' + b'\x00\x00')

        if isinstance(message, RequestRandomModeStatusCommand):
            return self._encode_message(b'\x16\x00' + b'\x00\x00')

        if isinstance(message, SetRandomModeCommand):
            is_active = b'\x00'
            if message.is_active:
                is_active = b'\x01'

            active_on_weekdays = 0
            for weekday in message.active_on_weekdays:
                active_on_weekdays += 2**weekday.value
            active_on_weekdays = active_on_weekdays.to_bytes(1, 'big')

            start_hour = message.start_hour.to_bytes(1, 'big')
            start_minute = message.start_minute.to_bytes(1, 'big')
            end_hour = message.end_hour.to_bytes(1, 'big')
            end_minute = message.end_minute.to_bytes(1, 'big')

            return self._encode_message(b'\x15\x00' + is_active + active_on_weekdays + start_hour + start_minute + end_hour + end_minute + b'\x00\x00')

        if isinstance(message, RequestMeasurementCommand):
            return self._encode_message(b'\x04\x00' + b'\x00\x00')

        if isinstance(message, RequestConsumptionOfLast12MonthsCommand):
            return self._encode_message(b'\x0c\x00' + b'\x00\x00')

        if isinstance(message, RequestConsumptionOfLast30DaysCommand):
            return self._encode_message(b'\x0b\x00' + b'\x00\x00')

        if isinstance(message, RequestConsumptionOfLast23HoursCommand):
            return self._encode_message(b'\x0a\x00' + b'\x00\x00')

        if isinstance(message, ResetConsumptionCommand):
            return self._encode_message(b'\x0f\x00' + b'\x02' + b'\x00\x00\x00\x00\x00')

        if isinstance(message, FactoryResetCommand):
            return self._encode_message(b'\x0f\x00' + b'\x00' + b'\x00\x00\x00\x00\x00')

        if isinstance(message, SetDeviceNameCommand):
            new_name = message.new_name
            if isinstance(new_name, str):
                new_name = new_name.encode()

            if len(new_name) > 18:
                raise Exception('name is too long - actual number of character: ' + str(len(new_name)) + ', maximum characters possible: 18')

            while len(new_name) < 18:
                new_name += b'\x00'

            return self._encode_message(b'\x02\x00' + new_name + b'\x00\x00')

        if isinstance(message, RequestDeviceSerialCommand):
            return self._encode_message(b'\x11\x00' + b'\x00\x00')

        if isinstance(message, AuthorizationNotification):
            was_successful = b'\x01'
            if message.was_successful:
                was_successful = b'\x00'

            return self._encode_message(b'\x17\x00' + was_successful + b'\x00\x00')

        if isinstance(message, ChangePinNotification):
            was_successful = b'\x01'
            if message.was_successful:
                was_successful = b'\x00'

            return self._encode_message(b'\x17\x00' + was_successful + b'\x01\x00')

        if isinstance(message, ResetPinNotification):
            was_successful = b'\x01'
            if message.was_successful:
                was_successful = b'\x00'

            return self._encode_message(b'\x17\x00' + was_successful + b'\x02\x00')

        if isinstance(message, PowerSwitchNotification):
            was_successful = b'\x01'
            if message.was_successful:
                was_successful = b'\x00'

            return self._encode_message(b'\x03\x00' + was_successful)

        if isinstance(message, LEDSwitchNotification):
            return self._encode_message(b'\x0f\x00' + b'\x05\x00')

        if isinstance(message, SynchronizeDateAndTimeNotification):
            was_successful = b'\x01'
            if message.was_successful:
                was_successful = b'\x00'

            return self._encode_message(b'\x01\x00' + was_successful)

        if isinstance(message, RequestedSettingsNotification):
            is_reduced_period = b'\x00'
            if message.is_reduced_period:
                is_reduced_period = b'\x01'

            normal_price_in_cent = message.normal_price_in_cent.to_bytes(1, 'big')
            reduced_period_price_in_cent = message.reduced_period_price_in_cent.to_bytes(1, 'big')

            reduced_period_start_time_in_minutes = message.reduced_period_start_time_in_minutes.to_bytes(2, 'big')
            reduced_period_end_time_in_minutes = message.reduced_period_end_time_in_minutes.to_bytes(2, 'big')

            is_led_active = b'\x00'
            if message.is_led_active:
                is_led_active = b'\x01'

            power_limit_in_watt = message.power_limit_in_watt.to_bytes(2, 'big')

            return self._encode_message(b'\x10\x00' + is_reduced_period + normal_price_in_cent + reduced_period_price_in_cent + reduced_period_start_time_in_minutes + reduced_period_end_time_in_minutes + is_led_active + b'\x00' + power_limit_in_watt)

        if isinstance(message, PowerLimitSetNotification):
            return self._encode_message(b'\x05\x00' + b'\x00')

        if isinstance(message, PricesSetNotification):
            return self._encode_message(b'\x0f\x00\x04' + b'\x00')

        if isinstance(message, ReducedPeriodSetNotification):
            return self._encode_message(b'\x0f\x00\x01' + b'\x00')

        if isinstance(message, RequestedTimerStatusNotification):
            timer_action = b'\x00'
            if message.is_timer_running:
                timer_action = b'\x02'
                if message.is_action_turn_on:
                    timer_action = b'\x01'

            target_second = message.target_second.to_bytes(1, 'big')
            target_minute = message.target_minute.to_bytes(1, 'big')
            target_hour = message.target_hour.to_bytes(1, 'big')
            target_day = message.target_day.to_bytes(1, 'big')
            target_month = message.target_month.to_bytes(1, 'big')
            target_year = message.target_year.to_bytes(1, 'big')

            original_timer_length_in_seconds = message.original_timer_length_in_seconds.to_bytes(3, 'big')

            return self._encode_message(b'\x09\x00' + timer_action + target_second + target_minute + target_hour + target_day + target_month + target_year + original_timer_length_in_seconds + b'\x00')

        if isinstance(message, TimerSetNotification):
            return self._encode_message(b'\x08\x00\x00')

        if isinstance(message, SchedulerRequestedNotification):
            schedulers_data = b''

            number_of_schedulers = len(message.scheduler_entries)
            for i in range(number_of_schedulers):
                scheduler_entry = message.scheduler_entries[i]
                scheduler = scheduler_entry.scheduler

                slot_id = scheduler_entry.slot_id.to_bytes(1, 'big')

                scheduler_data = self._encode_scheduler(scheduler) + b'\x00\x00' 
                checksum = (sum(scheduler_data)+0x14) & 0xff
                checksum = checksum.to_bytes(1, 'big')

                schedulers_data += slot_id + scheduler_data + checksum

            number_of_schedulers = number_of_schedulers.to_bytes(1, 'big')

            return self._encode_message(b'\x14\x00' + number_of_schedulers + schedulers_data)

        if isinstance(message, SchedulerSetNotification):
            was_successful = b'\x01'
            if message.was_successful:
                was_successful = b'\x00'

            return self._encode_message(b'\x13\x00' + was_successful + b'\x00\x00')

        if isinstance(message, RandomModeStatusRequestedNotification):
            is_active = b'\x00'
            if message.is_active:
                is_active = b'\x01'

            active_on_weekdays = 0
            for weekday in message.active_on_weekdays:
                active_on_weekdays += 2**weekday.value
            active_on_weekdays = active_on_weekdays.to_bytes(1, 'big')

            start_hour = message.start_hour.to_bytes(1, 'big')
            start_minute = message.start_minute.to_bytes(1, 'big')
            end_hour = message.end_hour.to_bytes(1, 'big')
            end_minute = message.end_minute.to_bytes(1, 'big')

            return self._encode_message(b'\x16\x00' + is_active + active_on_weekdays + start_hour + start_minute + end_hour + end_minute + b'\x00\x00')

        if isinstance(message, RandomModeSetNotification):
            was_successful = b'\x01'
            if message.was_successful:
                was_successful = b'\x00'

            return self._encode_message(b'\x15\x00' + was_successful + b'\x00')

        if isinstance(message, MeasurementRequestedNotification):
            is_power_active = b'\x00'
            if message.is_power_active:
                is_power_active = b'\x01'

            power_in_milliwatt = message.power_in_milliwatt.to_bytes(3, 'big')
            voltage_in_volt = message.voltage_in_volt.to_bytes(1, 'big')
            current_in_milliampere = message.current_in_milliampere.to_bytes(2, 'big')
            frequency_in_hertz = message.frequency_in_hertz.to_bytes(1, 'big')
            total_consumption_in_kilowatt_hour = message.total_consumption_in_kilowatt_hour.to_bytes(4, 'big')

            # suffix=b'\xff\xff' is missing in this notification
            return self._encode_message(b'\x04\x00' + is_power_active + power_in_milliwatt + voltage_in_volt + current_in_milliampere + frequency_in_hertz + b'\x00\x00' + total_consumption_in_kilowatt_hour, suffix=b'')

        if isinstance(message, ConsumptionOfLast12MonthsRequestedNotification):
            consumptions = b''

            # notification does not contain measurements for current months
            for i in range(1, len(message.consumption_n_months_ago_in_watt_hour)):
                consumption = message.consumption_n_months_ago_in_watt_hour[i]
                consumptions = consumption.to_bytes(3, 'big') + b'\x00' + consumptions

            return self._encode_message(b'\x0c\x00' + consumptions)

        if isinstance(message, ConsumptionOfLast30DaysRequestedNotification):
            consumptions = b''

            # notification does not contain measurements for today
            for i in range(1, len(message.consumption_n_days_ago_in_watt_hour)):
                consumption = message.consumption_n_days_ago_in_watt_hour[i]
                consumptions = consumption.to_bytes(3, 'big') + b'\x00' + consumptions

            return self._encode_message(b'\x0b\x00' + consumptions)

        if isinstance(message, ConsumptionOfLast23HoursRequestedNotification):
            consumptions = b''

            for consumption in message.consumption_n_hours_ago_in_watt_hour:
                consumptions = consumption.to_bytes(2, 'big') + consumptions

            return self._encode_message(b'\x0a\x00' + consumptions)

        if isinstance(message, ResetConsumptionNotification):
            return self._encode_message(b'\x0f\x00' + b'\x02' + b'\x00')

        if isinstance(message, FactoryResetNotification):
            return self._encode_message(b'\x0f\x00' + b'\x00' + b'\x00')

        if isinstance(message, DeviceNameSetNotification):
            return self._encode_message(b'\x02\x00' + b'\x00')

        if isinstance(message, DeviceSerialRequestedNotification):
            serial = message.serial.encode()

            return self._encode_message(b'\x11\x00' + serial + b'\x00\x00')

        raise Exception('Unsupported message ' + str(message))

