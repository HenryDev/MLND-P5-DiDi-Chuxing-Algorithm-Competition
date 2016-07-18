import random
from unittest import TestCase

from utilities.result_file_generator import make_result_file


class TestMakeResultFile(TestCase):
    def testGeneratorShouldWork(self):
        default_gap = []
        for _ in range(2838):
            default_gap.append(random.choice([0, 1]))
        # make_result_file(default_gap)
