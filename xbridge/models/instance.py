from models.context import Context


class Instance:

    def __init__(self,
                 facts_list_dict=None,
                 df=None,
                 facts=None,
                 contexts: [Context] = None,
                 module_code=None,
                 module_ref=None,
                 entity=None,
                 period=None,
                 filling_indicators=None,
                 base_currency=None,
                 units=None,
                 base_currency_unit=None,
                 pure_unit=None,
                 decimals_monetary=None,
                 decimals_percentage=None,
                 decimals_monetary_set=None,
                 decimals_percentage_set=None,
                 identifier_prefix=None
                 ):
        # self.path = path
        # self.root = etree.parse(self.path).getroot()

        self.__facts_list_dict = facts_list_dict
        self.__df = df
        self.__facts = facts
        self.__contexts: [Context] = contexts if contexts is not None else []
        self.__module_code = module_code
        self.__module_ref = module_ref
        self.__entity = entity
        self.__period = period
        self.__filing_indicators = filling_indicators
        self.__base_currency = base_currency
        self.__units = units
        self.__base_currency_unit = base_currency_unit
        self.__pure_unit = pure_unit
        self.__decimals_monetary = decimals_monetary
        self.__decimals_percentage = decimals_percentage
        self.__decimals_monetary_set = decimals_monetary_set if \
            decimals_monetary_set is not None else set()
        self._decimals_percentage_set = decimals_percentage_set if \
            decimals_percentage_set is not None else set()
        self._identifier_prefix = identifier_prefix

    @property
    def facts_list_dict(self):
        return self.__facts_list_dict

    @property
    def df(self):
        return self.__df

    @property
    def facts(self):
        return self.__facts

    @property
    def contexts(self):
        return self.__contexts

    @property
    def module_code(self):
        return self.__module_code

    @property
    def module_ref(self):
        return self.__module_ref

    @property
    def entity(self):
        return self.__entity

    @property
    def period(self):
        return self.__period

    @property
    def filling_indicators(self):
        return self.__filing_indicators

    @property
    def base_currency(self):
        return self.__base_currency

    @property
    def units(self):
        return self.__units

    @property
    def base_currency_unit(self):
        return self.__base_currency_unit

    @property
    def pure_unit(self):
        return self.__pure_unit

    @property
    def decimals_monetary(self):
        return self.__decimals_monetary

    @property
    def decimals_percentage(self):
        return self.__decimals_percentage

    @property
    def decimals_monetary_set(self):
        return self.__decimals_monetary_set

    @property
    def decimals_percentage_set(self):
        return self._decimals_percentage_set

    @property
    def identifier_prefix(self):
        return self._identifier_prefix

    def get_fact_list_dict(self) -> dict:
        pass
