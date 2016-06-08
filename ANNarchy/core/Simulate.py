from .Global import _network, config
from .Global import get_current_step, get_time, dt
from .Global import _warning, _error, _print
from math import ceil
import time

# Callbacks
_callbacks = [[]]
_callbacks_enabled = [True]


def simulate(duration, measure_time = False, callbacks=True, net_id=0):
    """
    Simulates the network for the given duration in milliseconds. The number of simulation steps is computed relative to the discretization step ``dt`` declared in ``setup()`` (default: 1ms)::

        simulate(1000.0)

    *Parameters*:

    * **duration**: the duration in milliseconds.
    * **measure_time**: defines whether the simulation time should be printed. Default: False.
    * **callbacks**: defines if the callback method (decorator ``every`` should be called). Default: True.
    """
    if not _network[net_id]['instance']:
        _error('simulate(): the network is not compiled yet.')
        

    # Compute the number of steps
    nb_steps = ceil(float(duration) / dt())

    if measure_time:
        tstart = time.time()

    if callbacks and _callbacks_enabled[net_id] and len(_callbacks[net_id]) > 0:
        _simulate_with_callbacks(duration, net_id)
    else:
        _network[net_id]['instance'].pyx_run(nb_steps)

    if measure_time:
        _print('Simulating', duration/1000.0, 'seconds of the network took', time.time() - tstart, 'seconds.')


def simulate_until(max_duration, population, operator='and', measure_time = False, net_id=0):
    """
    Runs the network for the maximal duration in milliseconds. If the ``stop_condition`` defined in the population becomes true during the simulation, it is stopped.

    One can specify several populations. If the stop condition is true for any of the populations, the simulation will stop ('or' function).

    Example::

        pop1 = Population( ..., stop_condition = "r > 1.0 : any")
        compile()
        simulate_until(max_duration=1000.0. population=pop1)

    *Parameters*:

    * **duration**: the maximum duration of the simulation in milliseconds.
    * **population**: the (list of) population whose ``stop_condition`` should be checked to stop the simulation.
    * **operator**: operator to be used ('and' or 'or') when multiple populations are provided (default: 'and').
    * **measure_time**: defines whether the simulation time should be printed (default=False).

    *Returns*:

    * the actual duration of the simulation in milliseconds.
    """
    if not _network[net_id]['instance']:
        _error('simulate_until(): the network is not compiled yet.')
        

    nb_steps = ceil(float(max_duration) / dt())
    if not isinstance(population, list):
        population = [population]


    if measure_time:
        tstart = time.time()

    nb = _network[net_id]['instance'].pyx_run_until(nb_steps, [pop.id for pop in population], True if operator=='and' else False)
    
    sim_time = float(nb) / dt()
    if measure_time:
        _print('Simulating', nb/dt()/1000.0, 'seconds of the network took', time.time() - tstart, 'seconds.')
    return sim_time


def step(net_id=0):
    """
    Performs a single simulation step (duration = ``dt``).
    """
    if not _network[net_id]['instance']:
        _error('simulate_until(): the network is not compiled yet.')
        

    _network[net_id]['instance'].pyx_step()


################################
## Decorators
################################

def callbacks_enabled(net_id=0):
    """
    Returns True if callbacks are enabled for the network. 
    """
    return _callbacks_enabled[net_id]

def disable_callbacks(net_id=0):
    """
    Disables all callbacks for the network. 
    """
    _callbacks_enabled[net_id] = False

def enable_callbacks(net_id=0):
    """
    Enables all declared callbacks for the network. 
    """
    _callbacks_enabled[net_id] = True

class every(object):
    """
    Decorator to declare a callback method that will be called periodically during the simulation.

    Example of setting increasing inputs to a population every 100 ms, with an offset of 90 ms (or -10 ms relative to the period)::

        @every(period=100., offset=-10.)
        def step_input(n):
            pop.I = float(n) / 100.

        simulate(10000.)

    ``step_input()`` will be called at times 90, 190, ..., 9990 ms during the call to ``simulate()``.

    The method must accept only ``n`` as parameter (an integer being 0 the first time the method is called, and incremented afterwards) and can not return anything.
    
    The times at which the method is called are relative to the time when ``simulate()`` is called (if ``t`` is already 150 before calling ``simulate()``, the first call will then be made at ``t=240`` with the previous example).

    If multiple callbacks are defined, they will be called in the order of their declaration if they occur at the same time.

    """

    def __init__(self, period, offset=0., wait=0.0, net_id=0):
        """
        *Parameters:*

        * **period**: interval in ms between two calls to the function. If less than ``dt``, will be called every step.
        * **offset**: by default, the first call to the method will be made at the start of the simulation. The offset delays the call within the period (default: 0.0). Can be negative, in which case it will be counted from the end of the period.
        * **wait**: allows to wait for a certain amount of time (in ms) before starting to call the method. 

        ``wait`` can be combined with ``offset``, so if ``period=100.``, ``offset=50.`` and ``wait=500.``, the first call will be made 550 ms after the call to ``simulate()``

        """
        self.period = max(float(period), dt())
        self.offset = min(float(offset), self.period)
        self.wait = max(float(wait), 0.0)
        _callbacks[net_id].append(self)

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        self.func = f
        return f


def _simulate_with_callbacks(duration, net_id=0):
    """
    replaces simulate() when call_backs are defined.
    """        
    t_start = get_current_step(net_id)
    length = int(duration/dt())

    # Compute the times
    times = []
    for c in _callbacks[net_id]:
        period = int(c.period/dt())
        offset = int(c.offset/dt()) % period
        wait = int(c.wait/dt())

        moments = range(t_start + wait + offset, t_start + length, period)
        n = 0
        for m in moments:
            times.append((m, c, n))
            n += 1

    # Sort the times to be surethey are in the right order.
    # TODO: make sure the callbacks stay in the declaration order.
    times = sorted(times)

    for time, callback, n in times:
        #print time, 
        # Advance the simulation to the desired time
        if time != get_current_step(net_id):
            _network[net_id]['instance'].pyx_run(time-get_current_step(net_id))
        # Call the callback
        callback.func(n)

    # Go to the end of the duration
    if get_current_step(net_id) < t_start + length:
        _network[net_id]['instance'].pyx_run(t_start + length - get_current_step(net_id))