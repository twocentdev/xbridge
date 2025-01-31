import unittest
from pathlib import Path

from models.taxonomy import Taxonomy
from parsers.taxonomies_parser import TaxonomyParser


class MyTestCase(unittest.TestCase):

    def test_first_test(self):
        taxonomy_path = Path(__file__).parent / "test_files" / "taxonomies_to_load" / "asset_encumbrance.zip"
        self.assertTrue(taxonomy_path.exists(), "Taxonomy path does not exists.")
        self.assertTrue(taxonomy_path.is_file(), "Taxonomy path is not a file.")
        tax = TaxonomyParser.from_json(taxonomy_path)
        self.assertTrue(isinstance(tax, Taxonomy))
        self.assertEqual(1, len(tax.modules))


if __name__ == '__main__':
    unittest.main()
