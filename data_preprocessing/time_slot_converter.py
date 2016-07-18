def datetimes_to_time_slots(datetime_data_frame):
    results = datetime_data_frame.applymap(datetime_to_time_slot)
    return results


def datetime_to_time_slot(datetime):
    time = datetime.split()[-1]
    digits = time.split(':')
    hour = int(digits[0]) * 60
    minute = int(digits[1]) / 10
    return hour + minute


def get_day_from_time_stamp(time_stamp):
    date = time_stamp.split()[0]
    date_numbers = date.split('-')
    day = date_numbers[-1]
    return int(day)


def get_day_and_slot_from_time_slot(time_slot):
    date_numbers = time_slot.split('-')
    day = date_numbers[2]
    slot = date_numbers[-1]
    return int(day), int(slot)
