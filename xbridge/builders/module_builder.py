from builders.table_builder import TableBuilder
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

    def build(self) -> Module:
        url_split = self.__url.split("/")
        if len(url_split) == 10:  # Architecture 2.0
            self.set_taxonomy_architecture("2.0")
            self.set_framework_code(url_split[6])
            self.set_framework_version(url_split[7])
        elif len(url_split) == 11:  # Architecture 1.0
            self.set_taxonomy_architecture("1.0")
            self.set_framework_code(url_split[7])
            self.set_framework_version(url_split[8])
        else:
            raise ValueError(
                f"Invalid taxonomy architecture: {len(url_split)}")

        mod = Module(self.__code,
                     self.__url,
                     self.__tables,
                     self.__taxonomy_architecture,
                     self.__framework_code,
                     self.__framework_version)
        return mod
