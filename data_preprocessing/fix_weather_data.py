import pandas as pd


# engine = engine = create_engine("mysql+mysqldb://bharat:bharat@localhost/di_di?unix_socket=/var/run/mysqld/mysqld.sock")
# con = engine.connect()

# weather_df = pd.read_sql_table('weather_info', con=con, parse_dates=True)


def fix_weather_data(df):
    df.set_index('Time', inplace=True)
    df = df.groupby(pd.TimeGrouper(freq='10Min')).mean()
    df.reset_index(inplace=True)
    df.fillna(method='bfill', inplace=True)
    return df

# fixed_weather_df = fixed_weather_df(weather_df)
