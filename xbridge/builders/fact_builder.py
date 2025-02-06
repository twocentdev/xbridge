from models.fact import Fact


class FactBuilder:

    def __init__(self):
        self.__metric = None
        self.__value = None
        self.__decimals = None
        self.__context = None
        self.__unit = None

    def set_metric(self, metric):
        self.__metric = metric

    def set_value(self, value):
        self.__value = value

    def set_decimals(self, decimals):
        self.__decimals = decimals

    def set_context(self, context):
        self.__context = context

    def set_unit(self, unit):
        self.__unit = unit

    def build(self):
        return Fact(self.__metric, self.__value, self.__decimals,
                    self.__context, self.__unit)
