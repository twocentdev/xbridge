from models.variable import Variable


class VariableBuilder:

    def __init__(self):
        self.__code: str = ""
        self.__dimensions = None
        self.__attributes = None

    def set_code(self, code: str):
        self.__code = code

    def set_dimensions(self, dimensions):
        self.__dimensions = dimensions

    def set_attributes(self, attributes):
        self.__attributes = attributes

    def build(self):
        return Variable(self.__code, self.__dimensions, self.__attributes)
    