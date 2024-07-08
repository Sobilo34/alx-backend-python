#!/usr/bin/env python3
"""
Creating asyncio.Tasks from regular functions
"""
import asyncio
from typing import List

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    Asynchronous coroutine that spawns task_wait_random n times with
    the specified max_delay and returns a list of the delays.

    Args:
        n (int): The number of times to spawn task_wait_random.
        max_delay (int): The maximum delay in seconds.

    Returns:
        List[float]: List of delays (float values) in ascending order.
    """
    delays = [task_wait_random(max_delay) for _ in range(n)]
    tasks = [await task for task in asyncio.as_completed(delays)]
    return tasks
