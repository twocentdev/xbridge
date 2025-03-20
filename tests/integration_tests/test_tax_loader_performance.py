import csv
import logging
import os
import time
import unittest

from pathlib import Path

from services.taxonomy_loader_service_handler import TaxonomyLoaderServiceHandler


class MyTestCase(unittest.TestCase):

    tax_path = Path(__file__).parent.parent / "test_files" / "performance_taxonomies"
    modules_path = tax_path / "modules"

    report = {}

    logging.basicConfig(
        format="[%(asctime)s][%(name)s][%(levelname)s] --> %(message)s",
        level=logging.DEBUG
    )

    def setUp(self) -> None:
        if not self.modules_path.exists():
            os.mkdir(self.modules_path)
        for file in self.modules_path.iterdir():
            self.__clean_up_subdir(file)

    def tearDown(self):
        with (open(self.modules_path / "report.csv", mode="w", newline="") as fl):
            fields = ["_id", "file", "timer"]
            csv_writer = csv.DictWriter(fl, fieldnames=fields)
            csv_writer.writeheader()
            counter = 0
            for k, v in self.report.items():
                csv_writer.writerow({"_id": counter, "file": k, "timer": v})
                counter += 1

    def test_taxonomy_7z_loader(self):
        tax_path: Path = self.tax_path / "Full_Taxonomy.7z"
        self.assertTrue(tax_path.exists(), "Taxonomy path not found")
        self.assertTrue(tax_path.is_file())
        start = time.time()
        TaxonomyLoaderServiceHandler.load(
            tax_path=tax_path,
            modules_path=self.modules_path
        )
        end = time.time()
        self.report[tax_path.name] = f"Time --> {end - start}s"

    def __clean_up_subdir(self, path: Path):
        if path.is_dir():
            for file in path.iterdir():
                self.__clean_up_subdir(file)
            os.rmdir(path)
        else:
            os.remove(path)


if __name__ == '__main__':
    unittest.main()
