#!/usr/bin/env python3
"""
Annotate a particular function’s parameters
"""
from typing import Union, Any, Sequence, List


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """
    Returns the first element of a list if it exists, otherwise None.
    """
    if lst:
        return lst[0]
    else:
        return None
