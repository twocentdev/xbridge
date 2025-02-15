import copy
import csv
import json
import os
from pathlib import Path

import pandas as pd

from models.dim_dom_map import DimDomMap
from models.filing_indicator import FilingIndicator
from models.instance import Instance
from models.module import Module
from models.table import Table


class InstanceSerializer:

    @staticmethod
    def to_csv_dpm_1_0(output_path: Path,
                       module: Module,
                       dim_dom_map: DimDomMap,
                       instance: Instance):
        # Create temp dir(s)
        meta_inf_dir = output_path / "META-INF"
        reports_dir = output_path / "reports"
        output_path.mkdir()
        meta_inf_dir.mkdir()
        reports_dir.mkdir()

        InstanceSerializer.__reports_to_json(meta_inf_dir / "reports.json")
        InstanceSerializer.__report_to_json(
            reports_dir / "report.json",
            module.url
        )
        InstanceSerializer.__params_to_csv(
            reports_dir / "parameters.csv",
            instance
        )

        reported_tables = InstanceSerializer.__filling_indicators(
            reports_dir / "FilingInidcators.csv",
            instance.filling_indicators
        )
        # Save each reported table
        for table in reported_tables:
            InstanceSerializer.__table_to_csv(
                reports_dir / f"{table.lower()}.csv",
                module.get_table(table.replace(".", "-")),
                dim_dom_map,
                instance
            )

    @staticmethod
    def __filling_indicators(output_path: Path,
                             filing_indicators: [FilingIndicator]
                             ) -> [str]:
        reported_tables = []
        with open(output_path, "w", newline="", encoding="utf-8") as fl:
            csv_writer = csv.writer(fl)
            csv_writer.writerow(["templateID", "reported"])
            for elem in filing_indicators:
                value = "true" if elem.value else "false"
                csv_writer.writerow([
                    elem.table,
                    value
                ])
                if elem.value:
                    reported_tables.append(elem.table)
        return reported_tables

    @staticmethod
    def __params_to_csv(output_path: Path, instance: Instance):
        # Workaround;
        # Developed for the EBA structure
        # output_path_parameters = temp_dir_path / "parameters.csv"
        parameters = {
            "entityID": instance.entity,
            "refPeriod": instance.period,
            "baseCurrency": instance.base_currency,
            "decimalsInteger": 0,
            "decimalsMonetary": (
                instance.decimals_monetary
                if instance.decimals_monetary
                else 0
            ),
            "decimalsPercentage": (
                instance.decimals_percentage
                if instance.decimals_percentage
                else 4
            ),
        }
        with open(output_path, "w", newline="",
                  encoding="utf-8") as fl:
            csv_writer = csv.writer(fl)
            csv_writer.writerow(["name", "value"])
            for k, v in parameters.items():
                csv_writer.writerow([k, v])

    @staticmethod
    def __report_to_json(output_path: Path, module_url: str):
        with open(output_path, "w", encoding="UTF-8") as fl:
            json.dump(
                {
                    "documentInfo": {
                        "documentType": "https://xbrl.org/CR/2021-02-03/xbrl-csv",
                        "extends": [module_url],
                    }
                },
                fl,
            )

    @staticmethod
    def __reports_to_json(output_path: Path):
        with open(output_path, "w", encoding="UTF-8") as fl:
            json.dump(
                {
                    "documentInfo": {
                        "documentType": "http://xbrl.org/PWD/2020-12-09/report-package"
                    }
                },
                fl,
            )

    @staticmethod
    def __table_to_csv(
            output_path: Path,
            table: Table,
            dim_dom_map: DimDomMap,
            instance: Instance):
        print(f"About to parse table {table.code}")
        ##Workaround:
        # To calculate the table code for abstract tables, we look whether the name
        # ends with a letter, and if so, we remove the last part of the code
        # Possible alternative: add metadata mapping abstract and concrete tables to
        # avoid doing this kind of corrections
        # Defining the output path and check if the table is reported
        # normalised_table_code = table.code.replace("-", ".")
        # if normalised_table_code[-1].isalpha():
        #     normalised_table_code = \
        #     normalised_table_code.rsplit(".", maxsplit=1)[0]
        # if normalised_table_code not in self._reported_tables:
        #     continue

        # datapoints = self._variable_generator(table)
        datapoints = InstanceSerializer.__table_to_df(table, instance)
        # Cleaning up the dataframe and sorting it
        datapoints = datapoints.rename(columns={"value": "factValue"})
        # Workaround
        # The enumerated key dimensions need to have a prefix like the one
        # Defined by the EBA in the JSON files. We take them from the taxonomy
        # Because EBA is using exactly those for the JSON files.
        for open_key in table.open_keys:
            # dim_name = dim_dom_map.get(open_key)
            try:
                dim_name = dim_dom_map.get_dom_for_dim(open_key)
            except ValueError:
                print(f"{open_key} not found in dim-dom-map.")
            # For open keys, there are no dim_names (they are not mapped)
            if dim_name and not datapoints.empty:
                datapoints[open_key] = dim_name + ":" + datapoints[
                    open_key].astype(str)
        datapoints = datapoints.sort_values(by=["datapoint"], ascending=True)
        # output_path_table = output_path / table.url
        # print(datapoints)
        if not datapoints.empty:
            datapoints.to_csv(output_path, index=False)

    @staticmethod
    def __table_to_df(table: Table, instance: Instance) -> pd.DataFrame:
        """
        Returns the dataframe with the CSV file for the table

        :param table: The table we use.
        """

        variable_columns = set(table.variable_columns)
        open_keys = set(table.open_keys)
        attributes = set(table.attributes)
        # instance_columns = set(instance.instance_df.columns)
        instance_columns = set(instance.df.columns)

        # If any open key is not in the instance, then the table cannot have
        # any datapoint
        if not open_keys.issubset(instance_columns):
            return pd.DataFrame(
                columns=["datapoint", "value"] + list(open_keys))

        # Determine the not relevant dims
        not_relevant_dims = instance_columns - variable_columns \
                            - open_keys - attributes
        not_relevant_dims = not_relevant_dims - {"value", "unit", "decimals"}

        instance_df = copy.copy(instance.df)
        for col in ["unit", "decimals"]:
            if col not in attributes and col in instance_df.columns:
                del instance_df[col]

        # Drop datapoints that have non-null values in not relevant dimensions
        # And drop the not relevant columns
        instance_df = instance_df[
            instance_df[list(not_relevant_dims)].isnull().all(axis=1)
        ]
        for dim in not_relevant_dims:
            del instance_df[dim]

        # Do the intersection and drop from datapoints the columns and records
        intersect_cols = variable_columns & instance_columns
        datapoint_df = table.variable_df
        for col in variable_columns - instance_columns:
            datapoint_df = datapoint_df[datapoint_df[col].isnull()]
            del datapoint_df[col]

        # Join the dataframes on the datapoint_columns
        table_df = pd.merge(
            datapoint_df, instance_df, on=list(intersect_cols), how="inner"
        )

        if len(table_df) == 0:
            return pd.DataFrame(columns=["datapoint", "value"])

        for col in intersect_cols:
            del table_df[col]
        open_keys_copy = copy.copy(open_keys)
        for open_key_name in open_keys_copy:
            if open_key_name not in table_df.columns:
                open_keys.remove(open_key_name)
        table_df.dropna(subset=list(open_keys), inplace=True)

        if 'unit' in attributes:
            table_df['unit'] = table_df['unit'].map(
                lambda x: instance.units[x], na_action="ignore")

        return table_df
