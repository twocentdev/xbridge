import unittest
from pathlib import Path

from models.taxonomy import Taxonomy
from parsers.taxonomies_parser import TaxonomyParser


class MyTestCase(unittest.TestCase):

    def test_OLD_parsers(self):
        taxonomy_path = Path(__file__).parent / "test_files" / "taxonomies_to_load" / "asset_encumbrance.zip"
        self.assertTrue(taxonomy_path.exists(), "Taxonomy path does not exists.")
        self.assertTrue(taxonomy_path.is_file(), "Taxonomy path is not a file.")
        tax = TaxonomyParser.old_from_json(taxonomy_path)
        self.assertTrue(isinstance(tax, Taxonomy))
        self.assertEqual(1, len(tax.modules))
        self.assertEqual(23, len(tax.modules[0].tables))

    def test_parsers(self):
        taxonomy_path = Path(__file__).parent / "test_files" / "taxonomies_to_load" / "asset_encumbrance.zip"
        self.assertTrue(taxonomy_path.exists(), "Taxonomy path does not exists.")
        self.assertTrue(taxonomy_path.is_file(), "Taxonomy path is not a file.")
        tax = TaxonomyParser.from_json(taxonomy_path)
        self.assertIsNotNone(tax, "No taxonomy was created")
        self.assertEqual(1, len(tax.modules))
        self.assertEqual(23, len(tax.modules[0].tables))

    def test_check_both_parsers(self):
        taxonomy_path = Path(__file__).parent / "test_files" / "taxonomies_to_load" / "asset_encumbrance.zip"
        OLD_tax = TaxonomyParser.old_from_json(taxonomy_path)
        tax = TaxonomyParser.from_json(taxonomy_path)
        self.assertEqual(OLD_tax, tax)
        self.assertEqual(len(OLD_tax.modules), len(tax.modules))
        self.assertEqual(len(OLD_tax.modules[0].tables), len(tax.modules[0].tables))
        self.assertEqual(len(OLD_tax.modules[0].tables[0].open_keys), len(tax.modules[0].tables[0].open_keys))
        self.assertEqual(len(OLD_tax.modules[0].tables[1].variables[0].attributes),
                         len(tax.modules[0].tables[1].variables[0].attributes))


if __name__ == '__main__':
    unittest.main()
