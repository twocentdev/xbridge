from builders.variable_builder import VariableBuilder
from models.variable import Variable


class VariablesParser:

    @staticmethod
    def from_json(var_key: str, var_json: {}) -> Variable:
        var_builder = VariableBuilder()
        var_builder.set_code(var_key)
        var_builder.set_dimensions(var_json["dimensions"])
        if "decimals" in var_json["dimensions"]:
            var_builder.set_attributes(var_json["decimals"])
        return var_builder.build()

    @staticmethod
    def from_serialized(var_json: dict) -> VariableBuilder:
        var_builder = VariableBuilder()
        modified_dimensions = {}
        for k, v in var_json["dimensions"].items():
            if ":" in k:
                k = k.split(":")[1]
                modified_dimensions[k] = v
            else:
                modified_dimensions[k] = v
        modified_json = var_json.copy()
        modified_json["dimensions"] = modified_dimensions
        var_builder.set_code(modified_json["code"])
        var_builder.set_dimensions(modified_dimensions["dimensions"])
        var_builder.set_attributes(modified_dimensions["attributes"])
        return var_builder

