#!/usr/bin/python3
"""
Annotate a particular function’s parameters
and return values with the appropriate types
"""
from typing import Iterable, List, Tuple, Sequence


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Returns a list of tuples, each containing an iterable and an int.
    """
    return [(i, len(i)) for i in lst]
