import unittest

from bitcoin_address_total import bitcoin_address_total


class BitcoinAddressTotalTest(unittest.TestCase):

    def test_bitcoin_address_total(self):
        num_tx, total_value = bitcoin_address_total()
        self.assertEqual(3, num_tx)
        self.assertEqual(0.01850649, float(total_value))


if __name__ == "__main__":
    unittest.main()
