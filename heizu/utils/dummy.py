# -*- coding: utf-8 -*-
"""
Filler data generators.
"""

# Standard Libraries
from typing import List, Optional
import string

# External Libraries
import pandas as pd
import numpy.random as npr


_all_ = ['simple_random_df']


def simple_random_df( rows: int,
                      columns: int,
                      dtype: Optional[str] = 'int',
                      names: Optional[List[str]] = None
                      ) -> pd.DataFrame:
    """Generate a random :class:`~pandas.DataFrame`.

    Content is defined by ``dtype``. It can be an  ``int``, a ``float``
    or any attribute from the ``string`` library; that is, for example,
    ``ascii_letters``, ``printable`` or ``ascii_uppercase``, to cite some.

    For number types, integers will range from 0 to 100 and floats from 0 to 1.

    Combines content from
    `recipe <https://stackoverflow.com/a/32752318/2806632>`_,
    `recipe <https://stackoverflow.com/a/18272249/2806632>`_,
    `recipe <https://stackoverflow.com/a/48399379/2806632>`_

    .. codeauthor:: Jaume Bonet <jaume.bonet@gmail.com>
    """
    if names is None:
        names = list(string.ascii_uppercase[:columns])
    if len(names) != columns:
        raise AttributeError('Number of columns should match amount of names.')

    top = 51
    if dtype not in ['int', 'float']:
        try:
            top = len(getattr(string, 'ascii_uppercase').split()[0]) - 1
        except AttributeError:
            raise AttributeError('If not int of float, request an attribute from the string library.')

    df = pd.DataFrame(npr.randint(0, top, size=(rows, columns)), columns=names)

    if dtype == 'int':
        return df
    if dtype == 'float':
        return df / 100

    return df.applymap(dict(zip(range(top + 1), getattr(string, dtype).split()[0])).get)
