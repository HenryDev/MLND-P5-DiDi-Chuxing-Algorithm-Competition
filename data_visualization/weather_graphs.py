from utilities.file_names import weather_file_01
from utilities.file_reader import read_weather_file
import matplotlib.pyplot as plot


def first_day():
    data = read_weather_file('../' + weather_file_01)
    data.hist()
    plot.show()


if __name__ == "__main__":
    first_day()
