from models.scenario import Scenario


class ScenarioBuilder:

    def __init__(self):
        self.__dimension = {}

    def set_dimension(self, key, value):
        self.__dimension[key] = value

    def build(self):
        return Scenario(self.__dimension)
