# -*- coding: utf-8 -*-
"""
Provide a system to translate columns into links for Jupyter.
"""

# Standard Libraries
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Union

# External Libraries
from Ipython.display import HTML
import pandas as pd
import yaml

@dataclass
class LinkedFrame(object):
    """Add links to cells in a :class:`~pandas:DataFrame` by means of a defined
    `url_translator` and a set of `rules`.


    """
    url_translator: Union[str, Path] = field(init=True)
    rules: Dict = field(init=True)

    def __post_init__(self):
        pass

    def display(self, df: pd.DataFrame) -> HTML:
        pass
