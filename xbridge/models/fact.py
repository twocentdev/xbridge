class Fact:

    def __init__(self,
                 metric=None,
                 value=None,
                 decimals=None,
                 context=None,
                 unit=None
                 ):
        self.__metric = metric
        self.__value = value
        self.__decimals = decimals
        self.__context = context
        self.__unit = unit

    @property
    def metric(self):
        return self.__metric

    @property
    def value(self):
        return self.__value

    @property
    def decimals(self):
        return self.__decimals

    @property
    def context(self):
        return self.__context

    @property
    def unit(self):
        return self.__unit
