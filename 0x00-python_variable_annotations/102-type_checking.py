#!/usr/bin/env python3
"""
Zoom array function
"""

from typing import Any, List, Tuple


def zoom_array(lst: Tuple, factor: int = 2) -> List:
    """
    Zoom in on the array by repeating each element by a given factor
    """
    zoomed_in: List = [
        item for item in lst
        for i in range(factor)
    ]
    return zoomed_in


array = [12, 72, 91]
zoom_2x = zoom_array(tuple(array))
zoom_3x = zoom_array(tuple(array), int(3.0))
