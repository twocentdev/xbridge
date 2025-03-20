import logging

import yaml
from pathlib import Path


logger = logging.getLogger(__name__)


class AppConfig:

    __config = {}

    @classmethod
    def load_config(cls, file_path: Path | str):
        logger.debug("About to load config")
        file_path = file_path if isinstance(file_path, Path) else Path(file_path)
        try:
            with open(file_path, mode="r") as fl:
                cls.__config = yaml.safe_load(fl)
        except FileNotFoundError:
            err_msg = f"Error loading config file. File not found."
            logger.fatal(err_msg)
            raise FileNotFoundError(err_msg)

    def get_properties(self):
        if len(self.__config.items()) == 0:
            logger.warning("No config loaded")
        return self.__config.keys()

    def get_value(self, name: str):
        if len(self.__config.items()) == 0:
            logger.warning("No config loaded")
        if name in self.__config.keys():
            logger.debug(f"Match property [{name}] --> {self.__config[name]}")
            return self.__config[name]
        else:
            logger.warning("Property not found")
            return None

    def update_config(self, name: str, value):
        if name not in self.__config.keys():
            logger.warning("Property not found. About to add it.")
        self.__config[name] = value
