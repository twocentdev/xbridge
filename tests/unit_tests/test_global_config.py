import logging
import unittest
from pathlib import Path

from others.app_config import AppConfig


class MyTestCase(unittest.TestCase):

    config_path = (Path(__file__).parent.parent / "test_files" /
                       "config" / "config.yaml")

    logging.basicConfig(
        format="[%(asctime)s][%(name)s][%(levelname)s] --> %(message)s",
        level=logging.INFO
    )

    def setUp(self):
        AppConfig.load_config(self.config_path)

    def test_load_config(self):
        app = AppConfig()
        self.assertEqual(8, len(app.get_properties()))

    def test_check_loaded_properties(self):
        app = AppConfig()
        self.assertTrue(isinstance(app.get_value("mode"), str))
        self.assertEqual("tax", app.get_value("mode"))
        self.assertTrue(isinstance(app.get_value("input_path"), str))
        self.assertEqual("sth", app.get_value("input_path"))
        self.assertTrue(isinstance(app.get_value("output_path"), str))
        self.assertEqual("None", app.get_value("output_path"))
        self.assertTrue(isinstance(app.get_value("modules_path"), str))
        self.assertEqual("other", app.get_value("modules_path"))
        self.assertTrue(isinstance(app.get_value("overwrite"), bool))
        self.assertEqual(False, app.get_value("overwrite"))
        self.assertTrue(isinstance(app.get_value("verbose"), bool))
        self.assertEqual(True, app.get_value("verbose"))
        self.assertTrue(isinstance(app.get_value("filters"), list))
        self.assertEqual(['www.eba.europe.com', 'cucumber', 1], app.get_value("filters"))

    def test_add_property(self):
        property_name = "vegetable"
        property_value = "cucumber"
        app = AppConfig()
        self.assertFalse(property_name in app.get_properties())
        app.update_config(property_name, property_value)
        self.assertTrue(property_name in app.get_properties())
        self.assertEqual(property_value, app.get_value(property_name))


if __name__ == '__main__':
    unittest.main()
