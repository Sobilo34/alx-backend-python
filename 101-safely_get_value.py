#!/usr/bin/env python3
"""
return values, add type annotations to the function
"""

from typing import Mapping, Any, TypeVar, Union

T = TypeVar('T')

def safely_get_value(dct: Mapping, key: Any, default: Union[T, None] = None) -> Union[Any, T]:
    """
    return values, add type annotations to the function
    """
    if key in dct:
        return dct[key]
    else:
        return default
