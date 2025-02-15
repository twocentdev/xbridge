import os
import unittest
from pathlib import Path
from sys import modules

from services.instance_parser_service_handler import \
    InstanceParserServiceHandler
from services.taxonomy_loader_service_handler import \
    TaxonomyLoaderServiceHandler


class MyTestCase(unittest.TestCase):

    taxonomy_path: Path = Path(__file__).parent / "test_files" / "taxonomies_to_load"
    modules_path: Path = taxonomy_path / "modules"

    def setUp(self):
        if self.modules_path.exists():  # Clean previous executions
            for file in self.modules_path.iterdir():
                os.remove(file)
            os.remove(self.modules_path)

    def test_taxonomy_load_all(self):
        self.assertTrue(self.taxonomy_path.exists(), "Taxonomy path does not exists")
        self.assertTrue(self.taxonomy_path.is_dir(), "Taxonomy path is not a directory")
        self.assertFalse(self.modules_path.exists(), "Modules dir should not exist")
        for file in self.taxonomy_path.iterdir():
            if "zip" in file.name:
                TaxonomyLoaderServiceHandler.load(file, self.modules_path)
        self.assertTrue(self.modules_path.exists(), "No modules dir found")
        self.assertTrue((self.modules_path / "index.json").exists(), "Index file not found")
        self.assertTrue((self.modules_path / "dim_dom_mapping.json").exists(), "Dim-Dom-Map not found")
        # Check COREP modules (DPM 2.0)
        self.assertTrue((self.modules_path / "corep_lr_corep_4.0.json").exists())
        self.assertTrue((self.modules_path / "corep_of_corep_4.0.json").exists())
        # Check AE modules (DPM 1.0)
        self.assertTrue((self.modules_path / "ae_its-005-2020_2022-03-01.json").exists())
        # Check DORA modules (DORA)
        self.assertTrue((self.modules_path / "dora_dora_4.0.json").exists())

    def test_taxonomy_loader_dpm_2_0(self):
        self.assertTrue(self.taxonomy_path.exists(), "Taxonomy path does not exists")
        self.assertTrue(self.taxonomy_path.is_dir(), "Taxonomy path is not a directory")
        self.assertFalse(self.modules_path.exists(), "Modules dir should not exist")
        TaxonomyLoaderServiceHandler.load(self.taxonomy_path / "corep_dpm_2_0.zip", self.modules_path)
        self.assertTrue(self.modules_path.exists(), "No modules dir found")
        self.assertTrue((self.modules_path / "index.json").exists(), "Index file not found")
        self.assertTrue((self.modules_path / "dim_dom_mapping.json").exists(), "Dim-Dom-Map not found")
        self.assertTrue((self.modules_path / "corep_lr_corep_4.0.json").exists())
        self.assertTrue((self.modules_path / "corep_of_corep_4.0.json").exists())

    def test_taxonomy_loader_dpm_1_0(self):
        self.assertTrue(self.taxonomy_path.exists(), "Taxonomy path does not exists")
        self.assertTrue(self.taxonomy_path.is_dir(), "Taxonomy path is not a directory")
        self.assertFalse(self.modules_path.exists(), "Modules dir should not exist")
        TaxonomyLoaderServiceHandler.load(self.taxonomy_path / "asset_encumbrance.zip", self.modules_path)
        self.assertTrue(self.modules_path.exists(), "No modules dir found")
        self.assertTrue((self.modules_path / "index.json").exists(), "Index file not found")
        self.assertTrue((self.modules_path / "dim_dom_mapping.json").exists(), "Dim-Dom-Map not found")
        self.assertTrue((self.modules_path / "ae_its-005-2020_2022-03-01.json").exists())

    def test_taxonomy_loader_dora(self):
        self.assertTrue(self.taxonomy_path.exists(), "Taxonomy path does not exists")
        self.assertTrue(self.taxonomy_path.is_dir(), "Taxonomy path is not a directory")
        self.assertFalse(self.modules_path.exists(), "Modules dir should not exist")
        TaxonomyLoaderServiceHandler.load(self.taxonomy_path / "dora.zip", self.modules_path)
        self.assertTrue(self.modules_path.exists(), "No modules dir found")
        self.assertTrue((self.modules_path / "index.json").exists(), "Index file not found")
        self.assertTrue((self.modules_path / "dim_dom_mapping.json").exists(), "Dim-Dom-Map not found")
        self.assertTrue((self.modules_path / "dora_dora_4.0.json").exists())


if __name__ == '__main__': \
        unittest.main()
