import os
import unittest
from pathlib import Path
from services.taxonomy_loader_service_handler import \
    TaxonomyLoaderServiceHandler


class MyTestCase(unittest.TestCase):

    input_path: Path = Path(__file__).parent / "test_files" / "taxonomies_to_load"
    modules_path: Path = input_path / "modules"

    def setUp(self) -> None:
        for file in self.modules_path.iterdir():
            os.remove(file)

    def test_taxonomy_loader_dpm_1_0(self):
        self.assertTrue(self.input_path.exists(), "Taxonomy path does not exists")
        self.assertTrue(self.input_path.is_dir(), "Taxonomy path is not a directory")
        TaxonomyLoaderServiceHandler.load(self.input_path / "asset_encumbrance.zip", self.modules_path)
        self.assertTrue(self.modules_path.exists(), "No modules dir found")
        self.assertTrue((self.modules_path / "index.json").exists(), "Index file not found")
        self.assertTrue((self.modules_path / "dim_dom_mapping.json").exists(), "Dim-Dom-Map not found")
        self.assertTrue((self.modules_path / "ae_its-005-2020_2022-03-01.json").exists())

    def test_taxonomy_loader_dpm_2_0(self):
        self.assertTrue(self.input_path.exists(), "Taxonomy path does not exists")
        self.assertTrue(self.input_path.is_dir(), "Taxonomy path is not a directory")
        TaxonomyLoaderServiceHandler.load(self.input_path / "corep_dpm_2_0.zip", self.modules_path)
        self.assertTrue(self.modules_path.exists(), "No modules dir found")
        self.assertTrue((self.modules_path / "index.json").exists(), "Index file not found")
        self.assertTrue((self.modules_path / "dim_dom_mapping.json").exists(), "Dim-Dom-Map not found")
        self.assertTrue((self.modules_path / "corep_lr_corep_4.0.json").exists())
        self.assertTrue((self.modules_path / "corep_of_corep_4.0.json").exists())

    def test_taxonomy_loader_dora(self):
        self.assertTrue(self.input_path.exists(), "Taxonomy path does not exists")
        self.assertTrue(self.input_path.is_dir(), "Taxonomy path is not a directory")
        TaxonomyLoaderServiceHandler.load(self.input_path / "dora.zip", self.modules_path)
        self.assertTrue(self.modules_path.exists(), "No modules dir found")
        self.assertTrue((self.modules_path / "index.json").exists(), "Index file not found")
        self.assertTrue((self.modules_path / "dim_dom_mapping.json").exists(), "Dim-Dom-Map not found")
        self.assertTrue((self.modules_path / "dora_dora_4.0.json").exists())


if __name__ == '__main__': \
        unittest.main()
