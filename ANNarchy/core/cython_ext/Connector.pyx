# distutils: language = c++

from libcpp.vector cimport vector

from ANNarchy.core.Random import RandomDistribution

cdef class CSR:

    def __init__(self):
        self.data = {}

    cdef add (self, int rk, vector[int] r, vector[float] w, vector[int] d):
        cdef list val
        val = []
        val.append(r)
        val.append(w)
        val.append(d)
        self.data[rk] = val

    def keys(self):
        return self.data.keys()

    cpdef get_data(self):
        return self.data

def all_to_all(int pre_size, int post_size, weights, delays, allow_self_connections):

    cdef CSR synapses
    cdef int post, pre, size_pre
    cdef list tmp
    cdef vector[int] r, d
    cdef vector[float] w

    synapses = CSR()

    # Determine the size of the the pre-field (the passed arguments already knows if it is the same population or not)
    if allow_self_connections:
        size_pre = pre_size
    else:
        size_pre = pre_size -1 

    for post in xrange(post_size):
        tmp = [i for i in xrange(pre_size)]
        if not allow_self_connections:
            tmp.remove(post)
        r = tmp
        if isinstance(weights, (int, float)):
            w = vector[float](size_pre, float(weights))
        elif isinstance(weights, RandomDistribution):
            w = list(weights.get_values(size_pre))
        if isinstance(delays, int):
            d = vector[int](size_pre, delays)
        elif isinstance(weights, RandomDistribution):
            d = list(delays.get_values(size_pre))
        synapses.add(post, r, w, d)

    return synapses

