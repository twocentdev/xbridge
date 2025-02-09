from models.module import Module
from models.table import Table


class ModuleBuilder:

    def __init__(self):
        self.__code: str = ""
        self.__url: str = ""
        self.__taxonomy_code: str = ""
        self.__date: str = ""
        self.__tables: [Table] = []
        self.__taxonomy_module_path: str = ""

    def set_code(self, code: str):
        self.__code = code

    def set_url(self, url: str):
        self.__url = url

    def set_taxonomy_code(self, taxonomy_code: str):
        self.__taxonomy_code = taxonomy_code

    def set_date(self, date: str):
        self.__date = date

    def add_table(self, table: Table):
        self.__tables.append(table)

    def set_taxonomy_module_path(self, taxonomy_module_path: str):
        self.__taxonomy_module_path = taxonomy_module_path

    def build(self) -> Module:
        if self.__date == "mod":
            self.set_date(self.__taxonomy_code.replace(".", "_"))
        else:
            self.set_date(self.__date.replace("-", "_"))
        mod = Module(self.__code, self.__url, self.__taxonomy_code, self.__date, self.__tables)
        mod.taxonomy_module_path = self.__taxonomy_module_path
        return mod