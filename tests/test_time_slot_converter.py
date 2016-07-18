from unittest import TestCase
import pandas

from data_preprocessing.time_slot_converter import *


class TestTimeSlotConverter(TestCase):
    def test_time_slot_to_timestamp(self):
        # print time_slot_to_timestamp()
        pass

    def test_datetimes_to_time_slots(self):
        datetimes = {'a': ['2016-01-01 23:40:00', '2016-01-01 23:50:00']}
        df = pandas.DataFrame(datetimes)
        slots = datetimes_to_time_slots(df)
        expected = pandas.DataFrame({'a': [1384, 1385]})
        self.assertTrue(pandas.DataFrame.equals(slots, expected))

    def test_datetime_to_time_slot(self):
        self.assertEqual(datetime_to_time_slot('2016-01-01 23:40:00'), 1384)

    def test_get_day_from_time_stamp(self):
        self.assertEqual(get_day_from_time_stamp('2016-01-01 00:00:00'), 01)

    def test_get_day_and_slot_from_time_slot(self):
        self.assertEqual(get_day_and_slot_from_time_slot('2016-01-23-46'), (23, 46))
