class Variable:
    """Class representing a variable as represented in the JSON files. Can return or extract the `dimension <https://www.xbrl.org/guidance/xbrl-glossary/#:~:text=a%20taxonomy.-,Dimension,-A%20qualifying%20characteristic>`_
    of the :obj:`variable <xbridge.taxonomy.Variable>`, create a dictionary using its attributes as keys or return a variable object from the
    preprocessed JSON file.


    :param code: The code of the variable.

    :param dimensions: the `dimensions <https://www.xbrl.org/guidance/xbrl-glossary/#:~:text=a%20taxonomy.-,Dimension,-A%20qualifying%20characteristic>`_ of the variable.

    :param attributes: The attributes related to the variable.

    """

    def __init__(self,
                 code: str="",
                 dimensions= {},
                 attributes= {}):
        if dimensions is None:
            dimensions = {}
        self.__code: str = code
        self.__dimensions = dimensions
        self.__attributes = attributes

    @property
    def code(self):
        return self.__code

    @property
    def dimensions(self):
        """Returns the `dimensions <https://www.xbrl.org/guidance/xbrl-glossary/#:~:text=a%20taxonomy.-,Dimension,-A%20qualifying%20characteristic>`_ of a variable"""
        return self.__dimensions

    @dimensions.setter
    def dimensions(self, value):
        self.__dimensions = value

    @property
    def attributes(self):
        return self.__attributes

    @attributes.setter
    def attributes(self, value):
        self.__attributes = value

    def to_dict(self):
        """Returns a dictionary with the attributes"""
        return {
            "code": self.code,
            "dimensions": self.dimensions,
            "attributes": self.attributes,
        }

    def __repr__(self) -> str:
        return f"<Variable - {self.code}>"

    def __eq__(self, other):
        if not isinstance(other, Variable):
            return NotImplemented
        return (
            self.code == other.code
            and self.dimensions == other.dimensions
            and self.attributes == other.attributes
        )