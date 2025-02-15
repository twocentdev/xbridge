import sys
import unittest
from pathlib import Path

import taxonomy_loader


class MyTestCase(unittest.TestCase):

    def test_load_dpm_2_0(self):
        taxonomy_path = Path(__file__).parent / "test_files" / "taxonomies_to_load"
        sys.argv.append(str(taxonomy_path / "corep_dpm_2_0.zip"))
        taxonomy_loader.main()

    def test_load_dora(self):
        taxonomy_path = Path(__file__).parent / "test_files" / "taxonomies_to_load"
        sys.argv.append(str(taxonomy_path / "dora.zip"))
        taxonomy_loader.main()

if __name__ == '__main__':
    unittest.main()
