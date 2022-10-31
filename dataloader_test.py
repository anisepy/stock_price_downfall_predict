import unittest

from dataloader import yfloader


class MainTest(unittest.TestCase):
    def test_dataloader(self):
        st_c = "139480.KS"
        s_d = "2018-01-01"
        e_d = "2022-08-31"
        self.assertEqual(yfloader(st_c, s_d, e_d), "done")  # pragma: no cover


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
