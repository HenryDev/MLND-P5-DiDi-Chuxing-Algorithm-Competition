from unittest import TestCase

from data_preprocessing.fix_weather_data import fix_weather_data
from StringIO import StringIO

from utilities.file_reader import read_weather_file


class TestFixWeatherData(TestCase):
    def test_fix_weather_data(self):
        weather_data = '''
        2016-01-01 00:00:28	1	4.0	177
        2016-01-01 00:05:24	1	3.0	177
        2016-01-01 00:10:08	1	3.0	177
        '''
        data_file = StringIO(weather_data)
        df = read_weather_file(data_file)
        # fixed_data = fix_weather_data(df)
        # self.assertEqual(len(fixed_data), 2)
