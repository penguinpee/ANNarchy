from NeuralField import *
import numpy as np
cimport numpy as np
from datetime import datetime
import math

def run(InputPop, FocusPop):

    cdef int w = 20
    cdef int h = 20
    
    cdef float angle = 0.0
    cdef float radius = 0.5
    cdef float sigma = 2.0
    
    
    cdef int i, idx
    cdef float cw, ch, dist, value

    cdef np.ndarray data = np.zeros(w*h)

    for i in xrange (10000):
        t_start = datetime.now()

        angle += 1.0/5000.0

        cw = w / 2.0 * ( 1.0 + radius * np.cos(2 * math.pi * angle ) )
        ch = h / 2.0 * ( 1.0 + radius * np.sin(2 * math.pi * angle ) )

        for x in xrange(w):
            for y in xrange(h):
                dist = (x-cw)**2 + (y-ch)**2
                value = 0.5 * np.exp(-dist/2.0/sigma**2)
                idx = x+y*w
                data[idx] = value

        InputPop.cyInstance.baseline = data
        
        simulate(1)
        t_end = datetime.now()
        print t_end-t_start
