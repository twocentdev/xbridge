import unittest
from pathlib import Path
from zipfile import ZipFile

from pandas.plotting import table

from parsers.tables_parser import TablesParser


class MyTestCase(unittest.TestCase):

    def test_search_tables_dpm_2_0(self):
        tax_path = Path(__file__).parent / "test_files" / "taxonomies_to_load" / "corep_dpm_2_0.zip"
        self.assertTrue(tax_path.exists(), "Taxonomy file not found")
        with ZipFile(tax_path, mode="r") as zip_file:
            for file in zip_file.namelist():
                if TablesParser.file_is_table(file):
                    print(file)

if __name__ == '__main__':
    unittest.main()
