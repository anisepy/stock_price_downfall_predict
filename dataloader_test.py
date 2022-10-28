import unittest

from dataloader import yfloader


class MainTest(unittest.TestCase):
    def test_dataloader(self):
        self.assertEqual(yfloader("139480.KS", "2018-01-01", "2022-08-31"), "done")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
