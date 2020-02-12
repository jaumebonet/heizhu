# -*- coding: utf-8 -*-
"""
Extended input manipulations.
"""

# Standard Libraries
import os.path as op
import re
from io import StringIO
from pathlib import Path
from functools import partial
from typing import Callable, Union, List, Optional

# External Libraries
import pandas as pd


_all_ = ['multi_read', 'read_between']


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

    .. codeauthor:: Jaume Bonet <jaume.bonet@gmail.com>
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


def read_between( read_fx: Callable,
                  infile: Union[str, Path],
                  start_pattern: Optional[str] = None,
                  end_pattern: Optional[str] = None,
                  include_pattern: bool = False,
                  **kwargs
                  ) -> pd.DataFrame:
    """

    .. codeauthor:: Jaume Bonet <jaume.bonet@gmail.com>
    """
    idata = []
    refseq = r'({0}.*?{1})' if include_pattern else r'{0}(.*?){1}'
    refseq = refseq.format('' if start_pattern is None else start_pattern,
                           '' if end_pattern is None else end_pattern)
    with open(infile) as fp:
        for result in re.findall(refseq, fp.read(), re.S):
                idata.extend(result)
    return read_fx(StringIO(''.join(idata)), **kwargs)


def is_file_and_content( fl: Union[str, Path] ) -> bool:
    """Check that a file exists and has content.
    """
    fl = str(fl)
    return op.isfile(fl) and op.getsize(fl) > 0
