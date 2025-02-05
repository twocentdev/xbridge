from models.dim_dom_map import DimDomMap


class DimDomMapBuilder:

    def __init__(self):
        self.__map = {}

    def add_dom_for_dim(self, dim: str, dom: str):
        self.__map[dim] = dom

    def build(self) -> DimDomMap:
        map_ = DimDomMap()
        for dim, dom in self.__map.items():
            map_.add_mapping(dim, dom)
        return map_
