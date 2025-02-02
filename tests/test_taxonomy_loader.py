import json
import os
import sys
import unittest
from pathlib import Path
from zipfile import ZipFile

import taxonomy_loader
from converter import INDEX_FILE

MODULES_PATH = Path(__file__).parent.parent / "xbridge" / "modules"
MODULES_ZIP = MODULES_PATH / "modules.zip"


class MyTestCase(unittest.TestCase):

    def setUp(self):
        # Clean Zip /modules.zip
        if MODULES_ZIP.exists():
            os.remove(MODULES_ZIP)

        # Zip /modules dir
        with ZipFile(MODULES_ZIP, mode="w") as modules_zip:
            for filename in MODULES_PATH.iterdir():
                if filename.name.endswith(".zip"):  # Avoid to zip modules.zip or infinite loop
                    continue
                modules_zip.write(filename, arcname=filename.name)

        # Delete "original" JSON(s)
        for json_file in MODULES_PATH.iterdir():
            if not json_file.name.endswith(".json"):  # Avoid deleting non json files
                continue
            if json_file.name == "index.json":  # Avoid deleting index.json
                continue
            os.remove(json_file)

    def tearDown(self):
        # Restore json files
        for item in MODULES_PATH.iterdir():
            if not item.name.endswith(".zip"):
                os.remove(item)
        with ZipFile(MODULES_ZIP, mode="r") as modules_zip:
            modules_zip.extractall(MODULES_PATH)
        os.remove(MODULES_ZIP)

    def test_load_dpm_v01_taxonomy(self):
        # "Load" taxonomy
        taxonomy_path = Path(__file__).parent / "test_files" / "taxonomies_to_load" / "asset_encumbrance.zip"
        sys.argv.append(str(taxonomy_path))
        taxonomy_loader.main()

        # Assertions
        with ZipFile(MODULES_ZIP, mode="r") as modules_zip:
            ae_file_name = "ae_2022-03-01.json"
            self.assertTrue(ae_file_name in modules_zip.namelist())
            with open(MODULES_PATH / ae_file_name, mode="r") as ae:
                self.assertEqual(modules_zip.read(ae_file_name).decode("utf-8"), ae.read())
        with open(INDEX_FILE, mode="r") as index_json:
            ae_schema = "http://www.eba.europa.eu/eu/fr/xbrl/crr/fws/ae/its-005-2020/2022-03-01/mod/ae.xsd"
            index = json.load(index_json)
            self.assertTrue(ae_schema in index)

    def test_load_dpm_v02_taxonomy(self):
        # "Load" taxonomy
        try:
            taxonomy_path = Path(__file__).parent / "test_files" / "taxonomies_to_load" / "corep_dpm_2_0.zip"
            sys.argv.append(str(taxonomy_path))
            taxonomy_loader.main()
        except KeyError:
            self.fail("An unexpected error occurred")


if __name__ == '__main__':
    unittest.main()
