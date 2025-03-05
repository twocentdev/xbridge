import os
import unittest
from pathlib import Path

from services.instance_parser_service_handler import \
    InstanceParserServiceHandler
from services.taxonomy_loader_service_handler import \
    TaxonomyLoaderServiceHandler


class MyTestCase(unittest.TestCase):

    def test_taxonomy_loader_dpm_1_0(self):
        taxonomy_path: Path = Path(__file__).parent / "test_files" / \
                        "taxonomies_to_load" / "asset_encumbrance.zip"
        modules_dir: Path = taxonomy_path.parent / "modules"

        if modules_dir.exists():
            for file in os.listdir(modules_dir):
                os.remove(modules_dir / file)
            os.removedirs(modules_dir)

        self.assertTrue(taxonomy_path.exists(), "Taxonomy not found")
        self.assertTrue(taxonomy_path.is_file(),
                        "Given taxonomy is not a file"
                        )
        self.assertFalse(modules_dir.exists(), "This dir should not exist")
        TaxonomyLoaderServiceHandler.load(taxonomy_path, modules_dir)
        self.assertTrue(modules_dir.exists())
        self.assertTrue((modules_dir / "index.json").exists())
        self.assertTrue((modules_dir / "ae_its-005-2020_2022-03-01.json").exists())

    def test_taxonomy_loader_dora(self):
        taxonomy_path: Path = Path(__file__).parent / "test_files" / \
                              "taxonomies_to_load" / "dora.zip"
        modules_dir: Path = taxonomy_path.parent / "modules"

        if modules_dir.exists():
            for file in os.listdir(modules_dir):
                os.remove(modules_dir / file)
            os.removedirs(modules_dir)

        self.assertTrue(taxonomy_path.exists(), "Taxonomy not found")
        self.assertTrue(taxonomy_path.is_file(),
                        "Given taxonomy is not a file"
                        )
        self.assertFalse(modules_dir.exists(), "This dir should not exist")
        TaxonomyLoaderServiceHandler.load(taxonomy_path, modules_dir)
        self.assertTrue(modules_dir.exists())
        self.assertTrue((modules_dir / "index.json").exists())
        self.assertTrue((modules_dir / "dora_4_0.json").exists())
        self.assertTrue((modules_dir / "dora_2024_07_11.json").exists())

    def test_taxonomy_loader_dpm_2_0(self):
        taxonomy_path: Path = Path(__file__).parent / "test_files" / \
                        "taxonomies_to_load" / "corep_dpm_2_0.zip"
        modules_dir: Path = taxonomy_path.parent / "modules"

        if modules_dir.exists():
            for file in os.listdir(modules_dir):
                os.remove(modules_dir / file)
            os.removedirs(modules_dir)

        self.assertTrue(taxonomy_path.exists(), "Taxonomy not found")
        self.assertTrue(taxonomy_path.is_file(),
                        "Given taxonomy is not a file"
                        )
        self.assertFalse(modules_dir.exists(), "This dir should not exist")
        TaxonomyLoaderServiceHandler.load(taxonomy_path, modules_dir)
        self.assertTrue(modules_dir.exists())
        self.assertTrue((modules_dir / "index.json").exists())
        self.assertTrue((modules_dir / "corep_lr_4_0.json").exists())
        self.assertTrue((modules_dir / "corep_of_4_0.json").exists())

    def test_instance_loader_dpm_1_0(self):
        instance_path = Path(__file__).parent / "test_files" / \
                        "instances_to_parse_standard" / \
                        "12345123451234512345_ES_AE_AE_2025-01-31_20250124111336000.xbrl"
        output_path = instance_path.parent
        modules_path = Path(__file__).parent.parent / "xbridge" / "modules"
        self.assertTrue(instance_path.exists(), "Instance not found")
        InstanceParserServiceHandler.parse(
            instance_path,
            modules_path,
            output_path
        )

    def test_taxonomy_loader_filtered_with_match(self):
        taxonomy_path: Path = Path(__file__).parent / "test_files" / \
                        "taxonomies_to_load" / "asset_encumbrance.zip"
        modules_dir: Path = taxonomy_path.parent / "modules"
        filter: [str] = ["www.eba.europa.eu/eu/fr/xbrl/crr/fws/corep",
                         "www.eba.europa.eu/eu/fr/xbrl/crr/fws/ae"]

        if modules_dir.exists():
            for file in os.listdir(modules_dir):
                os.remove(modules_dir / file)
            os.removedirs(modules_dir)

        self.assertTrue(taxonomy_path.exists(), "Taxonomy not found")
        self.assertTrue(taxonomy_path.is_file(),
                        "Given taxonomy is not a file"
                        )
        self.assertFalse(modules_dir.exists(), "This dir should not exist")
        TaxonomyLoaderServiceHandler.load(taxonomy_path, modules_dir, filter)
        self.assertTrue(modules_dir.exists())
        self.assertTrue((modules_dir / "index.json").exists())
        self.assertTrue((modules_dir / "ae_its-005-2020_2022-03-01.json").exists())

    def test_taxonomy_loader_filtered_withou_match(self):
        taxonomy_path: Path = Path(__file__).parent / "test_files" / \
                        "taxonomies_to_load" / "asset_encumbrance.zip"
        modules_dir: Path = taxonomy_path.parent / "modules"
        filter: [str] = ["www.eba.europa.eu/eu/fr/xbrl/crr/fws/corep"]

        if modules_dir.exists():
            for file in os.listdir(modules_dir):
                os.remove(modules_dir / file)
            os.removedirs(modules_dir)

        self.assertTrue(taxonomy_path.exists(), "Taxonomy not found")
        self.assertTrue(taxonomy_path.is_file(),
                        "Given taxonomy is not a file"
                        )
        self.assertFalse(modules_dir.exists(), "This dir should not exist")
        TaxonomyLoaderServiceHandler.load(taxonomy_path, modules_dir, filter)
        self.assertTrue(modules_dir.exists())
        self.assertTrue((modules_dir / "index.json").exists())
        self.assertFalse((modules_dir /
                      "ae_its-005-2020_2022-03-01.json").exists())


if __name__ == '__main__': \
        unittest.main()
