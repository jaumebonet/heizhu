# -*- coding: utf-8 -*-
"""
.. codeauthor:: Jaume Bonet <jaume.bonet@gmail.com>
"""
# Standard Libraries
import os.path as op
from pathlib import Path
from functools import partial
from typing import Callable, Union, List, Optional

# External Libraries
import pandas as pd


_all_ = ['multi_read']


def multi_read( read_fx: Callable,
                files: Union[List, str, Path],
                pattern: Optional[str] = None,
                **kwargs
                ) -> pd.DataFrame:
    """Execute a :mod:`pandas` reading function for multiple files.

    Adapted from `recipe <https://stackoverflow.com/a/13499853/2806632>`_.

    It should work with any reading function that:
        a) Returns a :class:`~pandas.DataFrame`.
        b) Has the file path as first parameter.
    """
    # Managing input
    if isinstance(files, str):
        files = Path(files)
    if isinstance(files, Path):
        pattern = r'*' if pattern is None else pattern
        files = files.glob(pattern)
    if isinstance(files, list):
        files = list(map(is_file_and_content, files))

    # map function and execute
    mapfunc = partial(read_fx, **kwargs)
    return pd.concat(list(map(mapfunc, files)), sort=False).reset_index(drop=True)


def is_file_and_content( fl: Union[str, Path] ) -> bool:
    """
    """
    fl = str(fl)
    return op.isfile(fl) and op.getsize(fl) > 0
