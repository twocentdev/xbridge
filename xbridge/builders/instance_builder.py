import pandas as pd

from models.instance import Instance


class InstanceBuilder:

    def __init__(self):
        self.__facts_list_dict = None
        self.__df = None
        self.__facts = []
        self.__contexts = None
        self.__module_code = None
        self.__module_ref = None
        self.__entity = None
        self.__period = None
        self.__filing_indicators = None
        self.__base_currency = None
        self.__units = None
        self.__base_currency_unit = None
        self.__pure_unit = None
        self.__decimals_monetary = None
        self.__decimals_percentage = None
        self.__decimals_monetary_set = set()
        self.__decimals_percentage_set = set()
        self.__identifier_prefix = None

    def set_facts_list_dict(self, facts_list_dict):
        self.__facts_list_dict = facts_list_dict

    def set_df(self, df):
        self.__df = df

    def set_facts(self, facts):
        self.__facts = facts

    def set_contexts(self, contexts):
        self.__contexts = contexts

    def set_module_code(self, module_code):
        self.__module_code = module_code

    def set_module_ref(self, module_ref):
        self.__module_ref = module_ref

    def set_entity(self, entity):
        self.__entity = entity

    def set_period(self, period):
        self.__period = period

    def set_filing_indicators(self, filling_indicators):
        self.__filing_indicators = filling_indicators

    def set_base_currency(self, base_currency):
        self.__base_currency = base_currency

    def set_units(self, units):
        self.__units = units

    def set_base_currency_unit(self, base_currency_unit):
        self.__base_currency_unit = base_currency_unit

    def set_pure_unit(self, pure_unit):
        self.__pure_unit = pure_unit

    def set_decimals_monetary(self, decimals_monetary):
        self.__decimals_monetary = decimals_monetary

    def set_decimals_percentage(self, decimals_percentage):
        self.__decimals_percentage = decimals_percentage

    def add_decimals_monetary_set(self, decimals_monetary):
        self.__decimals_monetary_set.add(decimals_monetary)

    def add_decimals_percentage_set(self, decimals_percentage):
        self.__decimals_percentage_set.add(decimals_percentage)

    def set_identifier_prefix(self, identifier_prefix):
        self.__identifier_prefix = identifier_prefix

    def __create_df(self):
        """
        Generates a pandas DataFrame with the
        `facts <https://www.xbrl.org/guidance/xbrl-glossary/#:~:text=accounting%20standards%20body.-,Fact,-A%20fact%20is>`_
        of the instance file.
        """
        if self.__facts_list_dict is None:
            self.__create_facts_list_dict()
        self.__df = pd.DataFrame.from_dict(self.__facts_list_dict)
        df_columns = list(self.__df.columns)
        ##Workaround
        # Dropping period an entity columns because in current EBA architecture,
        # they have to be the same for all the facts. (Performance reasons)
        if "period" in df_columns:
            del self.__df["period"]
        if "entity" in df_columns:
            del self.__df["entity"]

    def __create_facts_list_dict(self):
        """
        Generates a list of dictionaries with the
        `facts <https://www.xbrl.org/guidance/xbrl-glossary/#:~:text=accounting%20standards%20body.-,Fact,-A%20fact%20is>`_
        of the instance file.
        """
        result = []
        for fact in self.__facts:
            fact_dict = fact.__dict__()

            context_id = fact_dict.pop("context")

            if context_id is not None:
                context = self.__contexts[context_id].__dict__()
                fact_dict.update(context)

            result.append(fact_dict)

        # self.__facts_list_dict = result
        self.set_facts_list_dict(result)

    def build(self) -> Instance:
        self.__create_facts_list_dict()
        self.__create_df()
        return Instance(
            self.__facts_list_dict,
            self.__df,
            self.__facts,
            self.__contexts,
            self.__module_code,
            self.__module_ref,
            self.__entity,
            self.__period,
            self.__filing_indicators,
            self.__base_currency,
            self.__units,
            self.__base_currency_unit,
            self.__pure_unit,
            self.__decimals_monetary,
            self.__decimals_percentage,
            self.__decimals_monetary_set,
            self.__decimals_percentage_set,
            self.__identifier_prefix
        )
