import csv
import logging
import os
import time
import unittest
from pathlib import Path

from others.app_config import AppConfig
from services.instance_parser_service_handler import \
    InstanceParserServiceHandler

logger = logging.getLogger(__name__)


class MyTestCase(unittest.TestCase):

    instances_path = Path(__file__).parent.parent / "test_files" / "instances_to_parse_batch"
    mod_path = Path(__file__).parent.parent.parent / "res"
    output_path = instances_path / "output"
    config_path = instances_path / "config.yaml"

    report = {}

    logging.basicConfig(
        format="[%(asctime)s][%(name)s][%(levelname)s] --> %(message)s",
        level=logging.DEBUG
    )

    def setUp(self):
        if not self.output_path.exists():
            os.mkdir(self.output_path)
        for file in self.output_path.iterdir():
            self.__clean_up_subdir(file)

    def tearDown(self):
        with (open(self.output_path / "report.csv", mode="w", newline="") as fl):
            fields = ["_id", "file", "status", "comment"]
            csv_writer = csv.DictWriter(fl, fieldnames=fields)
            csv_writer.writeheader()
            counter = 0
            for k, v in self.report.items():
                csv_writer.writerow({"_id": counter, "file": k, "status": "Time" in v, "comment": v})
                counter+=1

    def test_parse_instances_batch(self):
        self.assertTrue(self.instances_path.exists(), "Instances path not found")
        self.assertTrue(self.instances_path.is_dir())
        self.assertTrue(self.mod_path.exists(), "Modules path not found")
        self.assertTrue(self.mod_path.is_dir())
        self.assertTrue(self.output_path.exists(), "Output dir not found")
        self.assertTrue(self.output_path.is_dir())

        AppConfig.load_config(self.config_path)
        app_config = AppConfig()
        app_config.update_config("filing_indicators", self.mod_path / "fil_ind_map.csv")

        for file in self.instances_path.iterdir():
            if file.suffix != ".xbrl":
                logger.warning(f"About to avoid file {file}")
                continue
            logger.info(f"About to parse instance: {file}")
            try:
                start = time.time()
                InstanceParserServiceHandler.parse(
                    inst_path=file,
                    modules_path=self.mod_path,
                    output_path=self.output_path
                )
                end = time.time()
                output_file = self.output_path / file.stem
                self.assertTrue(Path(output_file).exists(), "Instance not found")
                self.assertTrue(Path(output_file).is_dir())
                self.report[file.name] = f"Time --> {end - start}s"
            except Exception as e:
                logger.error(f"Cannot parse instance {file}")
                self.report[file.name] = e.args[0]

    def __clean_up_subdir(self, path: Path):
        if path.is_dir():
            for file in path.iterdir():
                self.__clean_up_subdir(file)
            os.rmdir(path)
        else:
            os.remove(path)


if __name__ == '__main__':
    unittest.main()
