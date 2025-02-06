class Scenario:

    def __init__(self, dimensions):
        self.__dimensions = dimensions

    @property
    def dimensions(self):
        return self.__dimensions

    def __repr__(self) -> str:
        return f"Scenario(dimensions={self.dimensions})"
