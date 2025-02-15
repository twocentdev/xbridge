"""
    File for development testing
"""
import os
from glob import glob
from pathlib import Path
from time import time

import pandas as pd

from xbridge.converter import Converter

if __name__ == "__main__":
    # INPUT_PATH_3_3 = Path(__file__).parent / "tests" / "test_files" / "sample_3_3"
    INSTANCE_PATH = Path.cwd()  / "input" / "dora_sample.xbrl"
    # INSTANCE_PATH = Path(__file__).parent / "tests" / "test_files" / "sample_3_2_phase1" / "test1_in.xbrl"

    start = time()
    converter = Converter(INSTANCE_PATH)
    initial = time()
    print(converter.convert(output_path="output/", headers_as_datapoints=True))
    end = time()
    print(f"Time to initialize: {initial - start}")
    print(f"Time to convert: {end - initial}")
    print(f"Total time: {end - start}")
