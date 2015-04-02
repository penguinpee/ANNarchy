# ANNarchy core
from .core.Global import *
from .core.Neuron import Neuron, RateNeuron, SpikeNeuron
from .core.Synapse import Synapse, RateSynapse, SpikeSynapse
from .core.Population import Population
from .core.SpecificPopulation import PoissonPopulation, SpikeSourceArray
from .core.Projection import Projection
from .core.Dendrite import Dendrite
from .core.Random import Uniform, DiscreteUniform, Normal, LogNormal, Gamma, Exponential
from .core.IO import save, load, load_parameter
from .core.Utils import raster_plot, smoothed_rate, histogram, population_rate, sparse_random_matrix
from .parser.Report import report
from .models import *
from .extensions import *

# Cython modules
try:
    from .core.cython_ext.Connector import CSR
except Exception as e:
    core.Global._print(e)
    core.Global._error('Could not import Cython modules. Try reinstalling ANNarchy.')

# ANNarchy compilation
from .generator import compile

# Generic imports
import numpy as np
import os, sys

# Version
__version__ = '4.4'
__release__ = '4.4.0'
core.Global._print( 'ANNarchy ' + __version__ + ' (' + __release__ + \
                   ') on ' + sys.platform + ' (' + os.name + ').' )
