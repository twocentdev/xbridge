from models.module import Module
from models.table import Table


class ModuleBuilder:

    def __init__(self):
        self.__code: str = ""
        self.__url: str = ""
        self.__taxonomy_code: str = ""
        self.__date: str = ""
        self.__tables: [Table] = []

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

    def build(self) -> Module:
        return Module(self.__code, self.__url, self.__taxonomy_code, self.__date, self.__tables)
    