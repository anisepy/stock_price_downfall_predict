import unittest

from downturn import downturn
import pandas as pd


test1 = pd.read_csv("data/dataloader_test.csv")


class MainTest(unittest.TestCase):
    def test_downturn(self):
        self.assertEqual(downturn(test1), "done")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
