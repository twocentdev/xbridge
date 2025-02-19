import os
import time
import unittest
from pathlib import Path

import api
from services.instance_parser_service_handler import \
    InstanceParserServiceHandler


class MyTestCase(unittest.TestCase):

    instance_path: Path = Path(__file__).parent / "test_files" / "performance_instances"
    modules_path: Path = Path(__file__).parent / "test_files" / "taxonomies_to_load" / "modules"
    execution_times = {}

    def setUp(self):
        self.assertTrue(self.instance_path.exists(), f"Input path does not exist")
        self.assertTrue(self.instance_path.is_dir(), f"Input path {self.instance_path} is not a dir")
        self.assertTrue(self.modules_path.exists(), f"Modules path does not exist.")
        self.assertTrue(self.modules_path.is_dir(), f"Modules path {self.modules_path} is not a dir")

    def tearDown(self):
        for inst, resume in self.execution_times.items():
            print(f"Executed {inst} --> {resume['time']}")
        self.execution_times = {}

    def test_performance_fork(self):
        for file in self.instance_path.iterdir():
            if "xbrl" not in file.name:
                continue
            print(f"About to parse {file.name}")
            start = time.time()
            InstanceParserServiceHandler.parse(file, self.modules_path, self.instance_path / "output_fork")
            end = time.time()
            print(f"Elapsed time for {file.name} is {end - start}")
            self.execution_times[file.name] = {"start": start, "end": end, "time": (end - start)}

    def test_performance_old(self):
        for file in self.instance_path.iterdir():
            if "xbrl" not in file.name:
                continue
            print(f"About to parse {file.name}")
            start = time.time()
            api.convert_instance(file, self.instance_path / "output_old")
            end = time.time()
            print(f"Elapsed time for {file.name} is {end - start}")
            self.execution_times[file.name] = {"start": start, "end": end, "time": (end - start)}


if __name__ == '__main__':
    unittest.main()
