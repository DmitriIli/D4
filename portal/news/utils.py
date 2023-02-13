from django.db import connection, reset_queries

import time
import functools


def query_debugger(func):
    @function.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()
        start_queries = len(connection.queries)

        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f'{func.__name__}')
        print(f'Queries quantity: {end_queries-start_queries}')
        print(f'Exicute time: {(end-start):.2f}')
    return inner_func
