from models.variable import Variable


class VariableBuilder:

    def __init__(self):
        self.__code: str = ""
        self.__dimensions = None
        self.__attributes = None
        self.__datapoint_dict = {}

    def set_code(self, code: str):
        self.__code = code

    def set_dimensions(self, dimensions):
        self.__dimensions = dimensions

    def set_attributes(self, attributes):
        self.__attributes = attributes

    def set_datapoint_dict(self, datapoint_dict: {}):
        self.__datapoint_dict = datapoint_dict

    def __extract_dimensions(self):
        if "dimensions" in self.__datapoint_dict.keys():
            self.__dimensions = self.__datapoint_dict["dimensions"]
        if "decimals" in self.__datapoint_dict:
            self.__attributes = self.__datapoint_dict["decimals"]

    def from_json(self, json):
        self.set_code(json["code"])
        processed_dimensions = {}
        for k, v in json["dimensions"].items():
            if ":" in k:
                processed_dimensions[k.split(":")[1]] = v
            else:
                processed_dimensions[k] = v
        self.set_dimensions(processed_dimensions)
        self.set_attributes(json["attributes"])

    def build(self):
        self.__extract_dimensions()
        return Variable(self.__code, self.__dimensions, self.__attributes)
    
