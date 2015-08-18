ANNarchy (Artificial Neural Networks architect) is a parallel and hybrid simulator for distributed rate-coded or spiking neural networks. The core of the library is written in C++ and distributed using openMP or CUDA. It provides an interface in Python for the definition of the networks. It is released under the [GNU GPL v2 or later](http://www.gnu.org/licenses/gpl.html).

The latest source code is available at:

[http://bitbucket.org/annarchy/annarchy](http://bitbucket.org/annarchy/annarchy)

The documentation is available online at:

[http://annarchy.readthedocs.org](http://annarchy.readthedocs.org)

A forum for discussion is set at:

[https://groups.google.com/forum/#!forum/annarchy](https://groups.google.com/forum/#!forum/annarchy)

**Citation**

If you use ANNarchy for your research, we would appreciate if you cite the following paper:

Vitay, J, Dinkelbach, HÜ and Hamker, FH (2015). ANNarchy: a code generation approach to neural simulations on parallel hardware. *Frontiers in Neuroinformatics* 9:19. [doi://10.3389/fninf.2015.00019](doi://10.3389/fninf.2015.00019)

**Authors**:

* Julien Vitay (julien.vitay@informatik.tu-chemnitz.de).
* Helge Ülo Dinkelbach (helge-uelo.dinkelbach@informatik.tu-chemnitz.de).
* Fred Hamker (fred.hamker@informatik.tu-chemnitz.de).


**Installation**:

ANNarchy can be installed using one of the following commands:

* With administrator permissions:

~~~~
sudo python setup.py install
~~~~

* In the home directory:

~~~~
python setup.py install --user
~~~~

* To install it in another repertory (e.g. `/path/to/repertory`):

~~~~
export PYTHONPATH=$PYTHONPATH:/path/to/repertory/lib/python2.7/dist-packages
python setup.py install --prefix=/path/to/repertory
~~~~

The export command (for bash, adapt it to your interpreter) should be placed into the `.bashrc` or `.bash_profile` file in the home directory.

**Platforms**:

* GNU/Linux
* MacOS X

**Dependencies**:

* g++ >= 4.6
* Python 2.7 or >= 3.3
* Cython >= 0.19
* Setuptools >= 0.6
* Numpy >= 1.8
* Sympy >= 0.7.4

Recommended:

* lxml >= 3.0
* Scipy >= 0.12
* Matplotlib >= 1.1
* PyQtGraph >= 0.9.8
