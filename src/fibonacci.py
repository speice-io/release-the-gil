import argparse
from collections import defaultdict
from threading import Thread
from time import monotonic_ns
from typing import List, DefaultDict

from numba import jit
from texttable import Texttable

from fibonacci_cython import cython_gil, cython_nogil


@jit(nopython=True, nogil=True)
def numba_nogil(n: int) -> int:
    if n <= 1:
        return n

    a = 0
    b = 1

    c = a + b
    for _i in range(2, n):
        a = b
        b = c
        c = a + b

    return c


@jit(nopython=True)
def numba_gil(n: int) -> int:
    if n <= 1:
        return n

    a = 0
    b = 1

    c = a + b
    for _i in range(2, n):
        a = b
        b = c
        c = a + b

    return c


def main(n: int = 1_000_000_000):
    # Pre-compile the numba variants
    numba_nogil(15)
    numba_gil(15)

    functions = [cython_gil, cython_nogil, numba_gil, numba_nogil]
    names = ["cython_gil", "cython_nogil", "numba_gil", "numba_nogil"]
    results_single: List[str] = []
    results: DefaultDict[str, List[str]] = defaultdict(list)

    for i, t1_function in enumerate(functions):
        t1_name = names[i]

        start = monotonic_ns()
        t1_function(n)
        end = monotonic_ns()
        runtime = str((end - start) / float(1_000_000)) + "ms"
        results_single.append(runtime)

        for j, t2_function in enumerate(functions):
            t1 = Thread(target=t1_function, args=[n])
            t2 = Thread(target=t2_function, args=[n])

            # While there's overhead in the thread start/join calls unrelated to
            # actual runtime, it's pretty small relative to total runtime
            start = monotonic_ns()

            # The order in which we start threads matters!
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            end = monotonic_ns()

            runtime = str((end - start) / float(1_000_000)) + "ms"
            results[t1_name].append(runtime)

    table = Texttable()
    table.header(names)
    table.add_row(results_single)
    print(table.draw())

    table = Texttable()
    table.header([""] + names)
    for main_name, results in results.items():
        table.add_row([main_name] + results)

    print(table.draw())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', help='Fibonacci number to calculate', default=1_000_000_000)
    cmdline = parser.parse_args()

    main(cmdline.n)
