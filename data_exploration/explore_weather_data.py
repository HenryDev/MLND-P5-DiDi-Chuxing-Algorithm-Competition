from utilities.file_names import weather_file_01
from utilities.file_reader import read_weather_file


def explore_weather_data():
    weather_data = read_weather_file('../' + weather_file_01)
    print weather_data.mode()


if __name__ == "__main__":
    explore_weather_data()
