cdef unsigned long fibonacci(unsigned long n) nogil:
    if n <= 1:
        return n

    cdef unsigned long a = 0, b = 1, c = 0

    c = a + b
    for _i in range(2, n):
        a = b
        b = c
        c = a + b

    return c


def cython_nogil(unsigned long n):
    with nogil:
        value = fibonacci(n)

    return value


def cython_gil(unsigned long n):
    return fibonacci(n)
