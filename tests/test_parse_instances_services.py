import logging
import unittest
from pathlib import Path

from services.instance_parser_service_handler import InstanceParserServiceHandler


class MyTestCase(unittest.TestCase):

    instance_path = Path(__file__).parent / "test_files" / "instances_to_parse_standard"
    modules_path = Path(__file__).parent.parent / "xbridge" / "modules"

    def test_parse_instance_all(self):
        logging.basicConfig(
            format="[%(asctime)s][%(name)s][%(levelname)s] --> %(message)s",
            level=logging.DEBUG
        )
        self.assertTrue(self.instance_path.exists(), "Instance path not found")
        self.assertTrue(self.instance_path.is_dir(), "Instance path is not dir")
        self.assertTrue(self.modules_path.exists(), "Module(s) path not found")
        self.assertTrue(self.modules_path.is_dir(), "Module(s) path is not dir")
        for file in self.instance_path.iterdir():
            if ".xbrl" in file.name:
                print(f"About to parse {file.name}")
                InstanceParserServiceHandler.parse(file, self.modules_path, self.instance_path / "output")

    def test_parse_instance_non_eba(self):
        logging.basicConfig(
            format="[%(asctime)s][%(name)s][%(levelname)s] --> %(message)s",
            level=logging.DEBUG
        )
        instance_path = Path(__file__).parent / "test_files" / \
                        "instances_to_parse_no_eba"
        self.assertTrue(instance_path.exists(), "Instance path not found")
        self.assertTrue(instance_path.is_dir(), "Instance path is not dir")
        self.assertTrue(self.modules_path.exists(), "Module(s) path not found")
        self.assertTrue(self.modules_path.is_dir(),
                        "Module(s) path is not dir")
        for file in instance_path.iterdir():
            if ".xbrl" in file.name:
                print(f"About to parse {file.name}")
                InstanceParserServiceHandler.parse(file, self.modules_path,
                                                   instance_path / "output")


if __name__ == '__main__':
    unittest.main()
