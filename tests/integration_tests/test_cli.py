import logging
import sys
import unittest

from cli.xbridge_cli import XBridgeCLI


class MyTestCase(unittest.TestCase):

    logging.basicConfig(
        format="[%(asctime)s][%(name)s][%(levelname)s] --> %(message)s",
        level=logging.DEBUG
    )

    def test_app_config_not_found(self):
        sys.argv = ["cucumber", "--verbose", "--config", "sth"]
        app = XBridgeCLI()
        self.assertEqual(-1, app.main())

    def test_invalid_mode(self):
        sys.argv = ["cucumber", "--verbose"]
        app = XBridgeCLI()
        self.assertEqual(-1, app.main())

    def test_tax_loader(self):
        pass

if __name__ == '__main__':
    unittest.main()
