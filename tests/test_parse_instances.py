import os
import unittest
from pathlib import Path

import api


INSTANCES_PATH = Path(__file__).parent / "test_files" / "instances_to_parse_standard"


class MyTestCase(unittest.TestCase):

    def test_parse_instance_to_standard_csv(self):
        # Clean files from previous executions
        zip_files = [file for file in INSTANCES_PATH.iterdir() if
                     file.name.endswith(".zip")]
        for zip_file in zip_files:
            os.remove(zip_file)

        self.assertTrue(INSTANCES_PATH.exists(), "Instances path does not exist")
        self.assertTrue(INSTANCES_PATH.is_dir(), "Instances path is not a dir")

        instances = [instance for instance in INSTANCES_PATH.iterdir() if instance.name.endswith(".xbrl")]
        for instance in instances:
            api.convert_instance(instance, INSTANCES_PATH)
            self.assertTrue(Path(INSTANCES_PATH) / (instance.stem + ".xbrl"))

        # TODO: should be more assertions


if __name__ == '__main__':
    unittest.main()
