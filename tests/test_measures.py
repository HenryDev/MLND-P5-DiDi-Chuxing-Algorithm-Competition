from unittest import TestCase

from utilities.measures import calculate_mape


class TestMeasures(TestCase):
    def test_mape_with_perfect_prediction(self):
        gaps = [1, 2, 3]
        predictions = [1, 2, 3]
        self.assertEqual(calculate_mape(gaps, predictions), 0)

    def test_mape_with_one_off(self):
        gaps = [1, 2, 3]
        predictions = [1, 2, 4]
        self.assertEqual(calculate_mape(gaps, predictions), 1 / 8514.)

    def test_mape_with_another_one_off(self):
        gaps = [1, 2, 4]
        predictions = [1, 2, 1]
        self.assertEqual(calculate_mape(gaps, predictions), 1 / 3784.)

    def test_mape_with_zero_gaps(self):
        gaps = [1, 0, 4]
        predictions = [1, 2, 1]
        self.assertEqual(calculate_mape(gaps, predictions), 1 / 3784.)

    def test_mape_with_dtr(self):
        # gaps = read_feature_file('../' + feature_files['file_01'])['nullOrders'].dropna()
        # max_depths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # x_train, y_train, x_test, y_test = wrapper()
        # predictions = find_best_depth(max_depths, x_train, x_test, y_train)
        # self.assertTrue(calculate_mape(gaps, predictions['prediction']) > 0)
        pass
