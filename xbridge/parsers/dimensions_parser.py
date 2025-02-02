class DimensionsParser:

    @staticmethod
    def extract_dimensions(self, datapoint_dict):
        """Extracts the `dimensions <https://www.xbrl.org/guidance/xbrl-glossary/#:~:text=a%20taxonomy.-,Dimension,-A%20qualifying%20characteristic>`_ for the variable"""
        dimensions = datapoint_dict["dimensions"]
        if "decimals" in datapoint_dict:
            self._attributes = datapoint_dict["decimals"]