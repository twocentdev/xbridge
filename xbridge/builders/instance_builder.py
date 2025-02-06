from models.instance import Instance


class InstanceBuilder:

    def __init__(self):
        self._facts_list_dict = None
        self._df = None
        self._facts = None
        self._contexts = None
        self._module_code = None
        self._module_ref = None
        self._entity = None
        self._period = None
        self._filing_indicators = None
        self._base_currency = None
        self._units = None
        self._base_currency_unit = None
        self._pure_unit = None
        self._decimals_monetary = None
        self._decimals_percentage = None
        self._decimals_monetary_set = set()
        self._decimals_percentage_set = set()
        self._identifier_prefix = None

    def set_facts_list_dict(self, facts_list_dict):
        self._facts_list_dict = facts_list_dict

    def set_df(self, df):
        self._df = df

    def set_facts(self, facts):
        self._facts = facts

    def set_contexts(self, contexts):
        self._contexts = contexts

    def set_module_code(self, module_code):
        self._module_code = module_code

    def set_module_ref(self, module_ref):
        self._module_ref = module_ref

    def set_entity(self, entity):
        self._entity = entity

    def set_period(self, period):
        self._period = period

    def set_filing_indicators(self, filling_indicators):
        self._filing_indicators = filling_indicators

    def set_base_currency(self, base_currency):
        self._base_currency = base_currency

    def set_units(self, units):
        self._units = units

    def set_base_currency_unit(self, base_currency_unit):
        self._base_currency_unit = base_currency_unit

    def set_pure_unit(self, pure_unit):
        self._pure_unit = pure_unit

    def set_decimals_monetary(self, decimals_monetary):
        self._decimals_monetary = decimals_monetary

    def set_decimals_percentage(self, decimals_percentage):
        self._decimals_percentage = decimals_percentage

    def add_decimals_monetary_set(self, decimals_monetary):
        self._decimals_monetary_set.add(decimals_monetary)

    def add_decimals_percentage_set(self, decimals_percentage):
        self._decimals_percentage_set.add(decimals_percentage)

    def set_identifier_prefix(self, identifier_prefix):
        self._identifier_prefix = identifier_prefix

    def build(self) -> Instance:
        return Instance(
            self._facts_list_dict,
            self._df,
            self._facts,
            self._contexts,
            self._module_code,
            self._module_ref,
            self._entity,
            self._period,
            self._filing_indicators,
            self._base_currency,
            self._units,
            self._base_currency_unit,
            self._pure_unit,
            self._decimals_monetary,
            self._decimals_percentage,
            self._decimals_monetary_set,
            self._decimals_percentage_set,
            self._identifier_prefix
        )
