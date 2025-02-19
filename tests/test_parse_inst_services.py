import unittest
from pathlib import Path

from services.instance_parser_service_handler import \
    InstanceParserServiceHandler


class MyTestCase(unittest.TestCase):

    def test_parse_dora(self):
        instance_path = Path(__file__).parent / "test_files" \
                        / "instances_to_parse_standard"
        modules_path = Path(__file__).parent / "test_files" \
                       / "taxonomies_to_load" / "modules"
        for tax_file in instance_path.iterdir():
            if "DORA" in tax_file.name:
                print(f"About to parse {tax_file}")
                InstanceParserServiceHandler.parse(
                    tax_file,
                    modules_path,
                    instance_path / "output"
                )


if __name__ == '__main__':
    unittest.main()
