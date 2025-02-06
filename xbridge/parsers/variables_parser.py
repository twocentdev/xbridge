from builders.variable_builder import VariableBuilder
from models.variable import Variable


class VariablesParser:

    @staticmethod
    def from_json(var_key: str, var_json: {}) -> Variable:
        var_builder = VariableBuilder()
        var_builder.set_code(var_key)
        var_builder.set_datapoint_dict(var_json)
        return var_builder.build()
