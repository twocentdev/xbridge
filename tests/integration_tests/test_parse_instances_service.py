import logging
import os
import unittest
from itertools import chain
from pathlib import Path

from others.app_config import AppConfig
from services.instance_parser_service_handler import InstanceParserServiceHandler


class MyTestCase(unittest.TestCase):

    eba_instances_path = Path(__file__).parent.parent / "test_files" / "instances_to_parse_standard"
    no_eba_instances_path = Path(__file__).parent.parent / "test_files" / "instances_to_parse_no_eba"
    modules_path = Path(__file__).parent.parent.parent / "res"

    logging.basicConfig(
        format="[%(asctime)s][%(name)s][%(levelname)s] --> %(message)s",
        level=logging.DEBUG
    )

    def setUp(self):
        config_path = Path(__file__).parent.parent / "test_files" / "config" / "config.yaml"
        AppConfig.load_config(config_path)
        app_config = AppConfig()
        app_config.update_config("filing_indicators", self.modules_path / "fil_ind_map.csv")
        if not (self.eba_instances_path / "output").exists():
            os.mkdir(self.eba_instances_path / "output")
        if not (self.no_eba_instances_path / "output").exists():
            os.mkdir(self.no_eba_instances_path / "output")
        for file in chain(
                (self.eba_instances_path / "output").iterdir(),
                (self.no_eba_instances_path / "output").iterdir()):
            self.__clean_up_subdir(file)

    def test_parse_instances_eba(self):
        self.assertTrue(self.eba_instances_path.exists(), "Instance path not found")
        self.assertTrue(self.eba_instances_path.is_dir(), "Instance path is not dir")
        self.assertTrue(self.modules_path.exists(), "Module(s) path not found")
        self.assertTrue(self.modules_path.is_dir(), "Module(s) path is not dir")
        for file in self.no_eba_instances_path.iterdir():
            if ".xbrl" in file.name:
                print(f"About to parse {file.name}")
                InstanceParserServiceHandler.parse(
                    inst_path=file,
                    modules_path=self.modules_path,
                    output_path=self.eba_instances_path / "output"
                )

    def test_parse_instances_non_eba(self):
        self.assertTrue(self.no_eba_instances_path.exists(), "Instance path not found")
        self.assertTrue(self.no_eba_instances_path.is_dir(), "Instance path is not dir")
        self.assertTrue(self.modules_path.exists(), "Module(s) path not found")
        self.assertTrue(self.modules_path.is_dir(),
                        "Module(s) path is not dir")
        for file in self.no_eba_instances_path.iterdir():
            if ".xbrl" in file.name:
                print(f"About to parse {file.name}")
                InstanceParserServiceHandler.parse(file, self.modules_path, self.no_eba_instances_path / "output")

    def __clean_up_subdir(self, path: Path):
        if path.is_dir():
            for file in path.iterdir():
                self.__clean_up_subdir(file)
            os.rmdir(path)
        else:
            os.remove(path)

if __name__ == '__main__':
    unittest.main()
