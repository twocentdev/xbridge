from models.taxonomy import Taxonomy
from modules import Module


class TaxonomyBuilder:

    def __init__(self):
        self.__modules: [Module] = []

    def add_module(self, module: Module):
        self.__modules.append(module)

    def build(self) -> Taxonomy:
        tax = Taxonomy()
        tax.modules = self.__modules
        return tax
