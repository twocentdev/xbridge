from zipfile import ZipFile

from builders.variable_builder import VariableBuilder
from models.variable import Variable


class VariablesParser:

    @staticmethod
    def from_json(var_key: str, var_json: {}) -> Variable:
        # print(f"About to parse {var_key} - {var_json}")
        var_builder = VariableBuilder()
        var_builder.set_code(var_key)
        var_builder.set_dimensions(var_json["dimensions"])
        if "decimals" in var_json:
            var_builder.set_attributes(var_json["decimals"])
        return var_builder.build()