"""
In general we assume in ANNarchy a distinct set of weights for each post-synaptic neuron.
However, operations like pooling or convolution are applied systematically for all pre-neurons within
a projection. Consequently, the required weight matrix need to be stored only once. This can
save computation time and especially memory space.

Contained classes:

* Pooling: implements the pooling operation
* Convolution: simple-, layer-wise and bank of filter convolution

Implementation note:

* the implemenation code was formerly in weightSharing.SharedProjection.
"""
from .Pooling import PoolingProjection
from .Convolve import ConvolutionProjection
from .Copy import CopyProjection

# Export only the instantiable classes
__all__ = ['PoolingProjection', 'ConvolutionProjection', 'CopyProjection']