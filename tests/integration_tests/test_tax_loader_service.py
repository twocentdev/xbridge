import logging
import os
import unittest
from pathlib import Path
from services.taxonomy_loader_service_handler import \
    TaxonomyLoaderServiceHandler


class MyTestCase(unittest.TestCase):

    input_path: Path = (Path(__file__).parent.parent / "test_files" /
                        "taxonomies_to_load")
    modules_path: Path = input_path / "modules"

    logging.basicConfig(
        format="[%(asctime)s][%(name)s][%(levelname)s] --> %(message)s",
        level=logging.DEBUG
    )

    def setUp(self) -> None:
        if not self.modules_path.exists():
            os.mkdir(self.modules_path)
        for file in self.modules_path.iterdir():
            self.__clean_up_subdir(file)

    def test_taxonomy_loader_dpm_1_0(self):
        tax_path: Path = self.input_path / "asset_encumbrance.zip"
        self.assertTrue(tax_path.exists(), "Taxonomy path does not exists")
        self.assertTrue(tax_path.is_file(), "Unexpected taxonomy path")
        TaxonomyLoaderServiceHandler.load(
            tax_path = tax_path,
            modules_path = self.modules_path
        )
        self.assertTrue(self.modules_path.exists(), "No modules dir found")
        self.assertTrue((self.modules_path / "index.json").exists(), "Index file not found")
        self.assertTrue((self.modules_path / "dim_dom_mapping.json").exists(), "Dim-Dom-Map not found")
        self.assertTrue((self.modules_path / "ae_its-005-2020_2022-03-01.json").exists())

    def test_taxonomy_loader_dpm_2_0(self):
        tax_path: Path = self.input_path / "corep_dpm_2_0.zip"
        self.assertTrue(tax_path.exists(), "Taxonomy path does not exists")
        self.assertTrue(tax_path.is_file(), "Unexpected taxonomy path")
        TaxonomyLoaderServiceHandler.load(
            tax_path= tax_path,
            modules_path= self.modules_path
        )
        self.assertTrue(self.modules_path.exists(), "No modules dir found")
        self.assertTrue((self.modules_path / "index.json").exists(), "Index file not found")
        self.assertTrue((self.modules_path / "dim_dom_mapping.json").exists(), "Dim-Dom-Map not found")
        self.assertTrue((self.modules_path / "corep_lr_corep_4.0.json").exists())
        self.assertTrue((self.modules_path / "corep_of_corep_4.0.json").exists())

    def test_taxonomy_loader_dora(self):
        tax_path: Path = self.input_path / "dora.zip"
        self.assertTrue(tax_path.exists(), "Taxonomy path does not exists")
        self.assertTrue(tax_path.is_file(), "Unexpected taxonomy path")
        TaxonomyLoaderServiceHandler.load(
            tax_path= tax_path,
            modules_path= self.modules_path
        )
        self.assertTrue(self.modules_path.exists(), "No modules dir found")
        self.assertTrue((self.modules_path / "index.json").exists(), "Index file not found")
        self.assertTrue((self.modules_path / "dim_dom_mapping.json").exists(), "Dim-Dom-Map not found")
        self.assertTrue((self.modules_path / "dora_dora_4.0.json").exists())

    def test_taxonomy_loader_unzip(self):
        tax_path: Path = self.input_path / "www.eba.europa.eu"
        self.assertTrue(tax_path.exists(), "Taxonomy path not found")
        self.assertTrue(tax_path.is_dir())
        TaxonomyLoaderServiceHandler.load(
            tax_path= tax_path,
            modules_path= self.modules_path
        )
        self.assertTrue((self.modules_path / "ae_its-005-2020_2022-03-01.json").exists())
        self.assertTrue((self.modules_path / "dim_dom_mapping.json").exists())
        self.assertTrue((self.modules_path / "index.json").exists())

    def test_taxonomy_7z_loader(self):
        tax_path: Path = self.input_path / "asset_encumbrance.7z"
        self.assertTrue(tax_path.exists(), "Taxonomy path not found")
        self.assertTrue(tax_path.is_file())
        TaxonomyLoaderServiceHandler.load(
            tax_path=tax_path,
            modules_path=self.modules_path
        )
        self.assertTrue((self.modules_path / "ae_its-005-2020_2022-03-01.json").exists())
        self.assertTrue((self.modules_path / "dim_dom_mapping.json").exists())
        self.assertTrue((self.modules_path / "index.json").exists())

    def test_taxonomy_loader_overwrite(self):
        tax_path: Path = self.input_path / "corep_dpm_2_0.zip"
        self.assertTrue(tax_path.exists(), "Taxonomy path not found")
        self.assertTrue(tax_path.is_file())
        TaxonomyLoaderServiceHandler.load(
            tax_path=tax_path,
            modules_path=self.modules_path
        )
        self.assertTrue(self.modules_path.exists(), "No modules dir found")
        self.assertTrue((self.modules_path / "index.json").exists(), "Index file not found")
        self.assertTrue((self.modules_path / "dim_dom_mapping.json").exists(), "Dim-Dom-Map not found")
        self.assertTrue((self.modules_path / "corep_lr_corep_4.0.json").exists())
        self.assertTrue((self.modules_path / "corep_of_corep_4.0.json").exists())

        tax_path: Path = self.input_path / "dora.zip"
        TaxonomyLoaderServiceHandler.load(
            tax_path=tax_path,
            modules_path=self.modules_path,
            overwrite=False
        )
        # Check both mods
        self.assertTrue(self.modules_path.exists(), "No modules dir found")
        self.assertTrue((self.modules_path / "index.json").exists(), "Index file not found")
        self.assertTrue((self.modules_path / "dim_dom_mapping.json").exists(), "Dim-Dom-Map not found")
        self.assertTrue((self.modules_path / "corep_lr_corep_4.0.json").exists())
        self.assertTrue((self.modules_path / "corep_of_corep_4.0.json").exists())
        self.assertTrue((self.modules_path / "index.json").exists(), "Index file not found")
        self.assertTrue((self.modules_path / "dim_dom_mapping.json").exists(), "Dim-Dom-Map not found")
        self.assertTrue((self.modules_path / "dora_dora_4.0.json").exists())

    def test_taxonomy_loader_single_filtered(self):
        tax_path: Path = (Path(__file__).parent.parent /
                          "test_files" / "performance_taxonomies" /
                          "Full_Taxonomy.7z")
        filters = ["www.eba.europa.eu/eu/fr/xbrl/crr/fws/ae"]

        self.assertTrue(tax_path.exists(), "Taxonomy path not found")
        self.assertTrue(tax_path.is_file())

        TaxonomyLoaderServiceHandler.load(
            tax_path=tax_path,
            modules_path=self.modules_path,
            overwrite=True,
            filters=filters
        )

        self.assertTrue(self.modules_path.exists(), "No modules dir found")
        self.assertTrue((self.modules_path / "index.json").exists(), "Index file not found")
        self.assertTrue((self.modules_path / "dim_dom_mapping.json").exists(), "Dim-Dom-Map not found")
        self.assertTrue((self.modules_path / "ae_its-005-2020_2022-03-01.json").exists())

        filters = ["www.eba.europa.eu/eu/fr/xbrl/crr/fws/dora"]
        TaxonomyLoaderServiceHandler.load(
            tax_path=tax_path,
            modules_path=self.modules_path,
            overwrite=False,
            filters=filters
        )

        self.assertTrue(self.modules_path.exists(), "No modules dir found")
        self.assertTrue((self.modules_path / "index.json").exists(), "Index file not found")
        self.assertTrue((self.modules_path / "dim_dom_mapping.json").exists(), "Dim-Dom-Map not found")
        self.assertTrue((self.modules_path / "ae_its-005-2020_2022-03-01.json").exists())
        self.assertTrue((self.modules_path / "dora_dora_4.0.json").exists())

    def test_taxonomy_loader_multi_filtered(self):
        tax_path: Path = (Path(__file__).parent.parent /
                          "test_files" / "performance_taxonomies" /
                          "Full_Taxonomy.7z")
        filters = ["www.eba.europa.eu/eu/fr/xbrl/crr/fws/ae",
                   "www.eba.europa.eu/eu/fr/xbrl/crr/fws/dora"]

        TaxonomyLoaderServiceHandler.load(
            tax_path=tax_path,
            modules_path=self.modules_path,
            overwrite=True,
            filters=filters
        )

        self.assertTrue(self.modules_path.exists(), "No modules dir found")
        self.assertTrue((self.modules_path / "index.json").exists(), "Index file not found")
        self.assertTrue((self.modules_path / "dim_dom_mapping.json").exists(), "Dim-Dom-Map not found")
        self.assertTrue((self.modules_path / "ae_its-005-2020_2022-03-01.json").exists())
        self.assertTrue((self.modules_path / "dora_dora_4.0.json").exists())


    def __clean_up_subdir(self, path: Path):
        if path.is_dir():
            for file in path.iterdir():
                self.__clean_up_subdir(file)
            os.rmdir(path)
        else:
            os.remove(path)

if __name__ == '__main__':
        unittest.main()
