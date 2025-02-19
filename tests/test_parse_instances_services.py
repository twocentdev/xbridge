import unittest
from pathlib import Path

from services.instance_parser_service_handler import InstanceParserServiceHandler


class MyTestCase(unittest.TestCase):

    instance_path = Path(__file__).parent / "test_files" / "instances_to_parse_standard"
    modules_path = Path(__file__).parent / "test_files" / "taxonomies_to_load" / "modules"

    def test_parse_instance_dpm_1_0(self):
        self.assertTrue(self.instance_path.exists(), "Instance path not found")
        self.assertTrue(self.instance_path.is_dir(), "Instance path is not dir")
        self.assertTrue(self.modules_path.exists(), "Module(s) path not found")
        self.assertTrue(self.modules_path.is_dir(), "Module(s) path is not dir")
        for file in self.instance_path.iterdir():
            if ".xbrl" in file.name and "DORA" in file.name:
                print(f"About to parse {file.name}")
                InstanceParserServiceHandler.parse(file, self.modules_path, self.instance_path / "output")


if __name__ == '__main__':
    unittest.main()
