import sys
import unittest
from pathlib import Path

import taxonomy_loader
from api import convert_instance


class MyTestCase(unittest.TestCase):

    def test_load_dpm_2_0(self):
        taxonomy_path = Path(__file__).parent / "test_files" / "taxonomies_to_load"
        sys.argv.append(str(taxonomy_path / "corep_dpm_2_0.zip"))
        taxonomy_loader.main()

    def test_load_dora(self):
        taxonomy_path = Path(__file__).parent / "test_files" / "taxonomies_to_load"
        sys.argv.append(str(taxonomy_path / "dora.zip"))
        taxonomy_loader.main()

    def test_instance_parser_dpm_1_0(self):
        instance_path = Path(__file__).parent / "test_files" \
                        / "instances_to_parse_standard"
        output_path = instance_path / "output"
        for instance in instance_path.iterdir():
            if "xbrl" in instance.name and "AE" in instance.name:
                convert_instance(instance, output_path)

    def test_instance_parser_dora(self):
        instance_path = Path(__file__).parent / "test_files" \
                        / "instances_to_parse_standard"
        output_path = instance_path / "output"
        for instance in instance_path.iterdir():
            if "xbrl" in instance.name:
                convert_instance(instance, output_path)

if __name__ == '__main__':
    unittest.main()
