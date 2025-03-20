import csv
import os
import time
import unittest

from pathlib import Path

from others.app_config import AppConfig
from services.instance_parser_service_handler import InstanceParserServiceHandler


class MyTestCase(unittest.TestCase):

    instance_path: Path = (Path(__file__).parent.parent / "test_files" /
                           "performance_instances")
    output_path: Path = instance_path / "output"
    modules_path: Path = Path(__file__).parent.parent.parent / "res"

    report = {}

    def setUp(self):
        config_path = (Path(__file__).parent.parent / "test_files" / "config"
                       / "config.yaml")
        AppConfig.load_config(config_path)
        app_config = AppConfig()
        app_config.update_config("filing_indicators",
                                 self.modules_path / "fil_ind_map.csv")
        if not self.output_path.exists():
            os.mkdir(self.output_path)
        for file in self.output_path.iterdir():
            self.__clean_up_subdir(file)

    def tearDown(self):
        with open(self.modules_path / "report.csv", mode="w", newline="") as fl:
            fields = ["_id", "file", "timer"]
            csv_writer = csv.DictWriter(fl, fieldnames=fields)
            csv_writer.writeheader()
            counter = 0
            for k, v in self.report.items():
                csv_writer.writerow({"_id": counter, "file": k, "timer": v})
                counter += 1

    def test_performance(self):
        filtered_files = filter(
            lambda x: x.name.endswith("xbrl"),
            self.instance_path.iterdir()
        )
        for file in filtered_files:
            print(f"About to parse {file.name}")
            start = time.time()
            InstanceParserServiceHandler.parse(
                inst_path=file,
                modules_path=self.modules_path,
                output_path=self.instance_path / "output"
            )
            end = time.time()
            print(f"Elapsed time for {file.name} is {end - start}")
            self.report[file.name] = f"Time --> {end - start}s"

    def __clean_up_subdir(self, path: Path):
        if path.is_dir():
            for file in path.iterdir():
                self.__clean_up_subdir(file)
            os.rmdir(path)
        else:
            os.remove(path)


if __name__ == '__main__':
    unittest.main()
