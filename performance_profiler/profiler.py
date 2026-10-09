from functools import wraps

from odoo.tools.profiler import Profiler


def profile_method(method=None, *, query=True):
    def decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            with Profiler(
                collectors=['sql'],
                db=None,
                description=f'{self._name}.{method.__name__}',
                log=False,
            ) as profiler:
                result = method(self, *args, **kwargs)

            sql_collector = next(
                collector
                for collector in profiler.collectors
                if collector.name == 'sql'
            )

            sql_entries = sql_collector.entries

            total_time_ms = profiler.duration * 1000
            sql_time_ms = sum(
                entry['time'] for entry in sql_entries
            ) * 1000

            python_time_ms = max(
                total_time_ms - sql_time_ms,
                0,
            )

            print(
                '\n\n'
                '[METHOD PERFORMANCE]\n'
                f'Model        : {self._name}\n'
                f'Method       : {method.__name__}\n'
                f'Total Time   : {total_time_ms:.2f} ms\n'
                f'Python Time  : {python_time_ms:.2f} ms\n'
                f'SQL Time     : {sql_time_ms:.2f} ms\n'
                f'SQL Queries  : {len(sql_entries)}\n',
                flush=True,
            )

            if query:
                if sql_entries:
                    print('SQL QUERIES:', flush=True)

                    for index, entry in enumerate(sql_entries, 1):
                        print(
                            f'\nQuery #{index} ({entry["time"] * 1000:.2f} ms)\n'
                            f'{entry["full_query"]}',
                            flush=True,
                        )
                else:
                    print('SQL QUERIES: None', flush=True)

            print('\n\n', flush=True)
            return result

        return wrapper

    if method is None:
        return decorator
    return decorator(method)


def profile_class(cls=None, *, query=True):
    """Apply @profile to every method defined in this class body."""

    def decorator(cls):
        # vars(cls) returns ONLY attributes defined in this class body.
        # Inherited methods are NOT in here — see notes below.
        for name, value in list(vars(cls).items()):
            # Skip dunder methods (__init__, __repr__, __str__, ...)
            if name.startswith('__') and name.endswith('__'):
                continue
            # Skip staticmethod / classmethod wrappers
            if isinstance(value, (staticmethod, classmethod)):
                continue
            # Skip non-callables (fields, constants, properties, ...)
            if not callable(value):
                continue

            setattr(cls, name, profile_method(query=query)(value))

        return cls

    if cls is None:
        return decorator
    return decorator(cls)
