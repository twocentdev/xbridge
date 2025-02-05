class DimDomMap:

    def __init__(self):
        self.__map = {}

    @property
    def map(self) -> dict:
        return self.__map

    def add_mapping(self, dim: str, dom: str):
        self.__map[dim] = dom

    def get_dom_for_dim(self, dim: str) -> str:
        if dim not in self.__map.keys():
            raise ValueError(f"Dimension {dim} not found")
        return self.__map[dim]
