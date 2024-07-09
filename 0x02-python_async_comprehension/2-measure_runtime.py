#!/usr/bin/env python3

""" Module that contains a coroutine named measure_runtime
that will execute async_comprehension four times in parallel
using asyncio.gather.
Coroutine will measure the total runtime and return it.
Explanation for how the total runtime is 10 seconds or less
should be included in the documentation.
"""

import asyncio
from time import time
from random import uniform
from typing import Generator, List

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """ Async Coroutine function that will execute async_comprehension
    four times in parallel using asyncio.gather.
    Coroutine will measure the total runtime and return it.
    """
    start_timeOfExec = time()
    async_exec = [async_comprehension() for num in range(4)]
    result = await asyncio.gather(*async_exec)
    end_timeOfExec = time()
    """ Total runtime explanation:
    - Each call to async_comprehension waits for approximately 10 seconds
        because it awaits 10 asynchronous sleeps of 1 second each in the
        async_generator.
    - Since measure_runtime executes async_comprehension four times
        in parallel using asyncio.gather, the total runtime is roughly
        10 seconds, as each call to async_comprehension takes approximately
        10 seconds to complete.
    - Therefore, the total runtime is approximately 10 seconds.
    """
    return end_timeOfExec - start_timeOfExec
