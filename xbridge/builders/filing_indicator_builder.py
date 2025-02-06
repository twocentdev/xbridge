from models.filing_indicator import FilingIndicator


class FilingIndicatorBuilder:

    def __init__(self):
        self.__value = None
        self.__table = None
        self.__context = None

    def set_value(self, value):
        self.__value = value

    def set_table(self, table):
        self.__table = table

    def set_context(self, context):
        self.__context = context

    def build(self):
        return FilingIndicator(self.__value, self.__table, self.__context)
