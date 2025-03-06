import os
import time
import unittest

from pathlib import Path
from services.instance_parser_service_handler import InstanceParserServiceHandler


class MyTestCase(unittest.TestCase):

    instance_path: Path = Path(__file__).parent / "test_files" / "performance_instances"
    output_path: Path = instance_path / "output"
    modules_path: Path = Path(__file__).parent.parent / "res"

    execution_times = {}

    def setUp(self):
        for file in self.output_path.iterdir():
            self.__clean_up_subdir(file)

    def tearDown(self):
        for inst, resume in self.execution_times.items():
            print(f"Executed {inst} --> {resume['time']}")
        self.execution_times = {}

    def test_performance(self):
        filtered_files = filter(
            lambda x: x.name.endswith("xbrl"),
            self.instance_path.iterdir()
        )
        for file in filtered_files:
            print(f"About to parse {file.name}")
            start = time.time()
            InstanceParserServiceHandler.parse(file, self.modules_path, self.instance_path / "output")
            end = time.time()
            print(f"Elapsed time for {file.name} is {end - start}")
            self.execution_times[file.name] = {"start": start, "end": end, "time": (end - start)}

    def __clean_up_subdir(self, path: Path) -> bool:
        if path.is_dir():
            for file in path.iterdir():
                self.__clean_up_subdir(file)
            os.rmdir(path)
        else:
            os.remove(path)

if __name__ == '__main__':
    unittest.main()
