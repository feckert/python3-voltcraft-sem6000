import enum

class Weekday(enum.Enum):
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6


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

def _format_hour_and_minute_as_time(hour, minute):
    return "{:02}:{:02}".format(hour, minute)


def _format_year_and_month(year, month):
    return "{:04}-{:02}".format(year, month)

def _list_values_to_enum(enum_class, list_of_values):
    list_of_enums = []
    for v in list_of_values:
        list_of_enums.append(enum_class(v))
    return list_of_enums

def _format_list_of_objects(format_object_lambda, list_of_objects):
    is_first = True
    formatted_string = "["
    for o in list_of_objects:
        if not is_first:
            formatted_string += ", "
        formatted_string += format_object_lambda(o)
        is_first = False
    formatted_string += "]"

    return formatted_string


def _parse_boolean(boolean_string):
    boolean_value = False

    if str(boolean_string).lower() == "true":
        boolean_value = True
    if str(boolean_string).lower() == "on":
        boolean_value = True
    if str(boolean_string).lower() == "1":
        boolean_value = True

    return boolean_value

def _parse_list(list_input):
    if type(list_input) == list:
        list_value = list_input
    if type(list_input) == str:
        list_value = list_input.split(",")

    for i in range(len(list_value)):
        if type(list_value[i]) == str:
            list_value[i] = list_value[i].strip()

    return list_value

def _parse_weekday(weekday):
    if isinstance(weekday, Weekday):
        return weekday

    if type(weekday) == int:
        return Weekday(weekday)

    weekday = weekday.lower()

    weekday_num = 0
    for weekday_str in ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]:
        if weekday_str in weekday or weekday == str(weekday_num):
            return Weekday(weekday_num)
        weekday_num += 1

    return None

def _parse_weekdays_list(weekdays_list):
    weekdays=[]

    weekday_values_list = _parse_list(weekdays_list)
    for weekday_value in weekday_values_list:
        weekday = _parse_weekday(weekday_value)
        if weekday is None:
            continue
        weekdays.append(weekday)

    return weekdays

