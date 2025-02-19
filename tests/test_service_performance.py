import os
import time
import unittest
from pathlib import Path

from services.instance_parser_service_handler import \
    InstanceParserServiceHandler


class MyTestCase(unittest.TestCase):

    def test_performance(self):
        instance_path: Path = Path(__file__).parent / "test_files" / \
                        "performance_instances"
        modules_path: Path = Path(__file__).parent / "test_files" / \
                             "taxonomies_to_load" / "modules"
        self.assertTrue(instance_path.exists(), f"Input path does not exist")
        self.assertTrue(instance_path.is_dir(),
                        f"Input path {instance_path} is not a dir")
        self.assertTrue(modules_path.exists(), f"Modules path does not exist.")
        self.assertTrue(modules_path.is_dir(),
                        f"Modules path {modules_path} is not a dir")
        execution_times = {}
        for file in instance_path.iterdir():
            if "xbrl" not in file.name:
                continue
            print(f"About to parse {file.name}")
            start = time.time()
            InstanceParserServiceHandler.parse(file, modules_path, instance_path / "output")
            end = time.time()
            print(f"Elapsed time for {file.name} is {end - start}")
            execution_times[file.name] = {"start": start, "end": end, "time": (end - start)}
        for inst, resume in execution_times.items():
            print(f"Executed {inst} --> {resume['time']}")


if __name__ == '__main__':
    unittest.main()
