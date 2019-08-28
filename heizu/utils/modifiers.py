# -*- coding: utf-8 -*-
"""
Filler data generators.
"""
# Standard Libraries
import copy
from typing import List, Optional, Union

# External Libraries
import pandas as pd


_all_ = ['split_rows']


def split_rows( df: pd.DataFrame,
                column_selectors: Union[str, List[str]],
                row_delimiter: Optional[str] = None
                ) -> pd.DataFrame:
    """Given a dataframe in which certain columns are lists, it splits these lists
    making new rows in the :class:`~pandas.DataFrame` out of itself.

    When multiple columns have lists of similar lengths, it assumes that same index
    positions on the list go in the same new row.

    :param df: Input data.
    :param column_selectors: List of columns containg same-sized lists.
    :param row_delimiter: If provided, instead of list, it assumes data are strings
        and uses the delimiter to make those strings into lists.

    Modified from
    `recipe <https://gist.github.com/jlln/338b4b0b55bd6984f883#gistcomment-2698588>`_,
    """
    # we need to keep track of the ordering of the columns
    def _split_list_to_rows(row, row_accumulator, column_selector, row_delimiter):
        split_rows = {}
        max_split = 0
        for column_selector in column_selectors:
            if row_delimiter is not None:
                split_row = row[column_selector].split(row_delimiter)
            else:
                split_row = copy.deepcopy(row[column_selector])
            split_rows[column_selector] = split_row
            if len(split_row) > max_split:
                max_split = len(split_row)

        for _ in range(max_split):
            new_row = row.to_dict()
            for column_selector in column_selectors:
                try:
                    new_row[column_selector] = split_rows[column_selector].pop(0)
                except IndexError:
                    new_row[column_selector] = ''
            row_accumulator.append(new_row)

    new_rows = []
    df.apply(_split_list_to_rows, axis=1, args=(new_rows, column_selectors, row_delimiter))
    new_df = pd.DataFrame(new_rows, columns=df.columns)
    return new_df
