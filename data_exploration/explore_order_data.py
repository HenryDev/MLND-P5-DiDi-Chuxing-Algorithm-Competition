from utilities.file_names import order_data_01, order_data_02
from utilities.file_reader import read_order_file


def explore_order_data_01():
    order_data = read_order_file('../' + order_data_01)
    print 'first 5 rows:'
    print order_data.head()
    print ''
    print 'number of null drivers:'
    print order_data.isnull().sum()
    print ''
    print 'describe'
    print order_data.describe()
    print ''
    print 'info'
    print order_data.info()


def second_file():
    data = read_order_file('../' + order_data_02)
    print '# of nulls'
    print data.isnull().sum()
    print ''
    print 'describe'
    print data.describe()


if __name__ == "__main__":
    # explore_order_data_01()
    second_file()
