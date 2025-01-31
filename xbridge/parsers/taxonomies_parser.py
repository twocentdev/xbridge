"""
Module with the taxonomy class, that serves to create the 
JSON files with the conversion instructions.

Each time the EBA releases a new taxonomy, the taxonomy_loader.py
module must be run to reflect the changes in the taxonomy.
"""

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from time import time
from zipfile import ZipFile

from lxml import etree

from builders.taxonomy_builder import TaxonomyBuilder
from models.taxonomy import Taxonomy
from parsers.modules_parser import ModulesParser
from xbridge.modules import Module

MODULES_FOLDER = Path(__file__).parent / "modules"
INDEX_PATH = MODULES_FOLDER / "index.json"
DIM_DOM_MAPPING_PATH = MODULES_FOLDER / "dim_dom_mapping.json"

class TaxonomyParser:

    @staticmethod
    def from_json(input_path: Path) -> Taxonomy:
        """Returns a Taxonomy object from a JSON taxonomy file"""
        tax_builder = TaxonomyBuilder()
        for module in ModulesParser.from_json(input_path):
            tax_builder.add_module(module)
        return tax_builder.build()
