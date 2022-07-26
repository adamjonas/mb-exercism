import hashlib
import warnings
import unittest

from get_block_header import get_block_header


class BlockHeaderTest(unittest.TestCase):

    def test_block_header(self):
        """Check the hash of the Signet block header 40000
        """
        # Disable ResourceWarning
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

        # Get block header 40000
        block_header = get_block_header(40000)

        # Check that the format of block_header is (hex) str
        # Hint: check the options for the RPC calls you're making (e.g. verbose mode)
        self.assertIsInstance(block_header, str)

        # Check the SHA1 hash of the block header against hardcoded value
        self.assertEqual(hashlib.sha1(bytes.fromhex(block_header)).hexdigest(), "b1dd5170be11166ae71f5f57f7d6481c29248603")


if __name__ == "__main__":
    unittest.main()
