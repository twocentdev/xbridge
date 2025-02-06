class FilingIndicator:
    """Class for the `filing <https://www.xbrl.org/guidance/xbrl-glossary/#2-other-terms-in-technical-or-common-use:~:text=data%20point.-,Filing,-The%20file%20or>`_ indicator of an instance. Returns the filing Indicator value and also a table with a
    :obj:`Context <xbridge.xml_instance.Context>`
    """

    def __init__(self, value=None, table=None, context=None):
        self.__value = value
        self.__table = table
        self.__context = context

    @property
    def value(self):
        return self.__value

    @property
    def table(self):
        return self.__table

    @property
    def context(self):
        return self.__context

    def __dict__(self):
        return {
            "value": self.value,
            "table": self.table,
            "context": self.context,
        }

    def __repr__(self) -> str:
        return (
            f"FilingIndicator(value={self.value}, "
            f"table={self.table}, context={self.context})"
        )
