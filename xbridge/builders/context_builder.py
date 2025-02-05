from models.context import Context


class ContextBuilder:

    def __init__(self):
        self.__id = None
        self.__entity = None
        self.__period = None
        self.__scenario = None

    def set_id(self, id):
        self.__id = id

    def set_entity(self, entity):
        self.__entity = entity

    def set_period(self, period):
        self.__period = period

    def set_scenario(self, scenario):
        self.__scenario = scenario

    def build(self):
        return Context(self.__id, self.__entity,
                       self.__period, self.__scenario)
