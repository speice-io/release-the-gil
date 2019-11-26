cdef void _unlock() nogil:
    with nogil:
        pass


def unlock():
    with nogil:
        _unlock()
