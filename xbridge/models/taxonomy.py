from models.module import Module
from models.table import Table
from models.variable import Variable


class Taxonomy:
    """
    Class representing an XBRL taxonomy
    """

    def __init__(self):
        self.__modules: [Module] = []

    @property
    def modules(self):
        return self.__modules.copy()

    @modules.setter
    def modules(self, modules: [Module]):
        self.__modules = modules

    def get_module(self, code: str):
        for module in self.__modules:
            if module.code == code:
                return module
        raise ValueError(f"Module with code {code} not found in the taxonomy")

    def get_variables_from_module(self, code):
        module = self.get_module(code)
        return module.get_variables()

    def __eq__(self, other):
        if not isinstance(other, Taxonomy):
            return NotImplemented
        return len(self.modules) == len(other.modules)