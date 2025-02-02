class Table:
    """Class representing an XBRL :obj:`table <xbridge.taxonomy.Table>` as defined in the JSON file.

    Its properties allow to return open keys, variables and attributes from the :obj:`table <xbridge.taxonomy.Table>`. It can also generate a
    variable dataframe or work with one already created.
    Finally, it can return a dictionary using its attributes or a :obj:`Table <xbridge.taxonomy.Table>` object from the preprocessed JSON file.

    It is used when module is loaded to collect the information associated to the variables and open keys
    belonging to the table.

    :param code: The code of the table.

    :param url: The table reference within the module.

    :param open_keys: Open key contained in the table.

    :param variables: the variables that belongs to the table.

    :param attributes: attributes related to the variables that can be extracted from the table.

    :param input_zip_path: Path to the file used as table.
    """

    def __init__(self, code=None, url=None, open_keys=None, variables=None, attributes=None, input_zip_path=None,):
        self.table_zip_path = input_zip_path # TODO: May fall from here. To builders?
        self.__code = code
        self.__url = url
        self.__open_keys = open_keys if open_keys is not None else []
        self.__variables = variables if variables is not None else []
        self.__attributes = attributes if attributes is not None else []
        self.__datapoint_df = None

    @property
    def code(self):
        return self.__code

    @property
    def url(self):
        return self.__url

    @property
    def open_keys(self):
        return self.__open_keys.copy()

    @property
    def variables(self):
        return self.__variables.copy()

    @property
    def attributes(self):
        return self.__attributes.copy()

    @property
    def variable_df(self):
        """
        Returns a dataframe with the :obj:`variable <xbridge.taxonomy.Variable>` and extensional context
        """
        return self.__datapoint_df

    @property
    def variable_columns(self):
        """
        Returns the columns for the :obj:`variable <xbridge.taxonomy.Variable>` dataframe
        """
        columns = set(self.variable_df.columns)
        columns.remove("datapoint")
        return columns

    def to_dict(self):
        """Returns a dictionary for the :obj:`table <xbridge.taxonomy.Table>`"""
        return {
            "code": self.code,
            "url": self.url,
            "open_keys": self.open_keys,
            "variables": [var.to_dict() for var in self.variables],
            "attributes": self.attributes,
        }

    def __repr__(self) -> str:
        return f"<Table - {self.code}>"

    def __eq__(self, other):
        if not isinstance(other, Table):
            return NotImplemented
        return (
            self.code == other.code
            and self.url == other.url
            and len(self.open_keys) == len(other.open_keys)
            and len(self.attributes) == len(other.attributes)
            and len(self.variables) == len(other.variables)
            and self.table_zip_path == other.table_zip_path
        )