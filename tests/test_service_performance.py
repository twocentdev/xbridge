import os
import time
import unittest
from pathlib import Path

from services.instance_parser_service_handler import \
    InstanceParserServiceHandler


class MyTestCase(unittest.TestCase):

    def test_performance(self):
        instance_path: Path = Path(__file__).parent / "test_files" / \
                        "instances_to_parse_standard"
        modules_path: Path = Path(__file__).parent / "test_files" / \
                             "performance_instances" / "modules"
        self.assertTrue(instance_path.exists(), f"Input path does not exist")
        self.assertTrue(instance_path.is_dir(),
                        f"Input path {instance_path} is not a dir")
        self.assertTrue(modules_path.exists(), f"Modules path does not exist.")
        self.assertTrue(modules_path.is_dir(),
                        f"Modules path {modules_path} is not a dir")
        start = time.time()
        file = instance_path / "01234012340123401234_ES_DORA_DORA_2025-02-28_20250205132659000.xbrl"
        InstanceParserServiceHandler.parse(
            file,
            modules_path,
            instance_path
        )
        end = time.time()
        #for file in os.listdir(instance_path):
        #    start = time.time()
        #    InstanceParserServiceHandler.parse(
        #        instance_path / file,
        #        modules_path,
        #        instance_path
        #    )
        #    end = time.time()
        print(f"Elapsed time for {file} is {end - start}")


if __name__ == '__main__':
    unittest.main()
