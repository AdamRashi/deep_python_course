import cProfile
import pstats
from io import StringIO


def profile_deco(func):
    """
    Декоратор, выполняющий прoфилирование всех вызовов декорируемой функции.
    После вызова функции, можно вывести статистику с помощью метода
    <название_функции>.print_stat()
    """

    stats = {}

    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()

        # cтатистику будем сортировать по общему времени
        # выполнения, учитывая вызовы вложенных функций

        if func.__name__ not in stats:
            stats[func.__name__] = pstats.Stats(pr)
        else:
            stats[func.__name__].add(pstats.Stats(pr))
            sort_by = pstats.SortKey.CUMULATIVE
            stats[func.__name__].sort_stats(sort_by)

        return result

    def print_stat(*args, **kwargs):
        if func.__name__ in stats:
            print(f"Profiling statistics for function {func.__name__}:")
            stats[func.__name__].print_stats(*args, **kwargs)

        else:
            print(f"Function {func.__name__} was never called.")

    wrapper.print_stat = print_stat

    return wrapper
