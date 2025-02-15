from models.module import Module
from models.table import Table


class ModuleBuilder:

    def __init__(self):
        self.__code: str = ""
        self.__url: str = ""
        self.__taxonomy_architecture = ""
        self.__framework_code = ""
        self.__framework_version = ""
        self.__tables: [Table] = []

    def set_code(self, code: str):
        self.__code = code

    def set_url(self, url: str):
        self.__url = url

    def set_taxonomy_architecture(self, taxonomy_architecture):
        self.__taxonomy_architecture = taxonomy_architecture

    def set_framework_code(self, framework_code):
        self.__framework_code = framework_code

    def set_framework_version(self, framework_version):
        self.__framework_version = framework_version

    def add_table(self, table: Table):
        self.__tables.append(table)

    def from_json(self, json: dict):
        # TODO: read mapping from json
        self.set_code(json["code"])
        self.set_url(json["url"])

    def build(self) -> Module:
        mod = Module(self.__code,
                     self.__url,
                     self.__tables,
                     self.__taxonomy_architecture,
                     self.__framework_code,
                     self.__framework_version)
        return mod
