#===============================================================================
#
#     BoldMonitor.py
#
#     This file is part of ANNarchy.
#
#     Copyright (C) 2018-2019  Helge Uelo Dinkelbach <helge.dinkelbach@gmail.com>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     ANNarchy is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#===============================================================================
from ANNarchy.core import Global
from ANNarchy.core.Population import Population
from ANNarchy.core.Monitor import Monitor

class BoldMonitor(Monitor):
    """
    Specialized monitor for populations. Transforms the signal *variables* into a BOLD signal.

    Using the hemodynamic model as described in:

    * Friston et al. 2000: Nonlinear Responses in fMRI: The Balloon Model, Volterra Kernels, and Other Hemodynamics
    * Friston et al. 2003: Dynamic causal modelling

    TODO: more explanations
    """
    def __init__(self, obj, variables=[], epsilon=1.0, alpha=0.3215, kappa=0.665, gamma=0.412, E_0=0.3424, V_0=0.02, tau_s=0.8, tau_f=0.4, tau_0=1.0368, period=None, period_offset=None, start=True, net_id=0):

        """
        *Parameters*:

        * **obj**: object to monitor. Must be a Population or PopulationView.

        * **variables**: single variable name or list of variable names to record (default: []).

        * **epsilon**: TODO (default: 1.0)

        * **alpha**: TODO (default: 0.3215)

        * **kappa**: TODO (default: 0.665)

        * **gamma**: TODO (default: 0.412)

        * **E_0**: TODO (default: 0.3424)

        * **V_0**: TODO (default: 0.02)

        * **tau_s**: TODO (default: 0.8)

        * **tau_f**: TODO (default: 0.4)

        * **tau_0**: TODO (default: 1.0368)

        * **period**: delay in ms between two recording (default: dt). Not valid for the ``spike`` variable of a Population(View).

        * **period_offset**: determines the moment in ms of recording within the period (default 0). Must be smaller than **period**.

        * **start**: defines if the recording should start immediately (default: True). If not, you should later start the recordings with the ``start()`` method.
        """

        if not isinstance(obj, Population):
            Global._error("BoldMonitors can only record Populations.")

        if Global._network[net_id]['compiled']:
            # HD (28th Jan. 2019): it is a bit unhandy to force the user to use BoldMonitors differently,
            # but to generate a bold monitor code for all variables possible beforehand,
            # as we do it for normal monitors, is not a suitable approach.
            Global._error("BoldMonitors need to be instantiated before compile.")

        super(BoldMonitor, self).__init__(obj, variables, period, period_offset, start, net_id)

        # Store the parameters
        self._epsilon = epsilon
        self._alpha = alpha
        self._kappa = kappa
        self._gamma = gamma
        self._E_0 = E_0
        self._V_0 = V_0
        self._tau_s = tau_s
        self._tau_f = tau_f
        self._tau_0 = tau_0


        # TODO: for now, we use the population id as unique identifier. This would be wrong,
        #       if multiple BoldMonitors could be attached to one population ...
        #
        # Without stimuli it's suitable to init v, q and f_out with 1.0
        self._specific_template = {
            'cpp': """
// BoldMonitor pop%(pop_id)s (%(pop_name)s)
class BoldMonitor%(pop_id)s : public Monitor{
public:
    BoldMonitor%(pop_id)s(std::vector<int> ranks, int period, int period_offset, long int offset)
        : Monitor(ranks, period, period_offset, offset) {

        E = std::vector<%(float_prec)s>( ranks.size(), E_0 );
        v = std::vector<%(float_prec)s>( ranks.size(), 1.0 );
        q = std::vector<%(float_prec)s>( ranks.size(), 1.0 );
        s = std::vector<%(float_prec)s>( ranks.size(), 0.0 );
        f_in = std::vector<%(float_prec)s>( ranks.size(), 1.0 );
        f_out = std::vector<%(float_prec)s>( ranks.size(), 1.0 );
    #ifdef _DEBUG
        std::cout << "BoldMonitor initialized (" << this << ") ... " << std::endl;
    #endif
    }

    ~BoldMonitor%(pop_id)s() = default;

    void record() {
        %(float_prec)s k1 = 7 * E_0;
        %(float_prec)s k2 = 2;
        %(float_prec)s k3 = 2*E_0 - 0.2;

        std::vector<%(float_prec)s> res = std::vector<%(float_prec)s>(ranks.size());
        int i = 0;
        for(auto it = ranks.begin(); it != ranks.end(); it++, i++) {
            %(float_prec)s u = pop%(pop_id)s.%(var_name)s[*it];

            E[i] = -pow(-E_0 + 1.0, 1.0/f_in[i]) + 1;
            f_out[i] = pow(v[i], 1.0/alpha);

            %(float_prec)s _v = (f_in[i] - f_out[i])/tau_0;
            %(float_prec)s _q = (E[i]*f_in[i]/E_0 - f_out[i]*q[i]/v[i])/tau_0;
            %(float_prec)s _s = epsilon*u - kappa*s[i] - gamma*(f_in[i] - 1);
            %(float_prec)s _f_in = s[i];

            v[i] += 0.001*dt*_v;
            q[i] += 0.001*dt*_q;
            s[i] += 0.001*dt*_s;
            f_in[i] += 0.001*dt*_f_in;

            res[i] = V_0*(k1*(-q[i] + 1) + k2*(-q[i]/v[i] + 1) + k3*(-v[i] + 1));
        }

        // store the result
        out_signal.push_back(res);

        // record intermediate variables
        rec_E.push_back(E);
        rec_f_out.push_back(f_out);
        rec_v.push_back(v);
        rec_q.push_back(q);
        rec_s.push_back(s);
        rec_f_in.push_back(f_in);

        // clear interim result
        res.clear();
    }

    long int size_in_bytes() {
        long int size_in_bytes = 0;

        // Computation Vectors
        size_in_bytes += E.capacity() * sizeof(%(float_prec)s);
        size_in_bytes += v.capacity() * sizeof(%(float_prec)s);
        size_in_bytes += q.capacity() * sizeof(%(float_prec)s);
        size_in_bytes += s.capacity() * sizeof(%(float_prec)s);
        size_in_bytes += f_in.capacity() * sizeof(%(float_prec)s);
        size_in_bytes += f_out.capacity() * sizeof(%(float_prec)s);

        // Record
        for(int i = 0; i < out_signal.size(); i++) {
            // all vectors should have the same top-level size ...
            size_in_bytes += out_signal[i].capacity() * sizeof(%(float_prec)s);
            size_in_bytes += rec_E[i].capacity() * sizeof(%(float_prec)s);
            size_in_bytes += rec_f_out[i].capacity() * sizeof(%(float_prec)s);
            size_in_bytes += rec_v[i].capacity() * sizeof(%(float_prec)s);
            size_in_bytes += out_signal[i].capacity() * sizeof(%(float_prec)s);
        }

        return size_in_bytes;
    }

    void clear() {
        //std::cout << "BoldMonitor::clear (" << this << ") ... " << std::endl;

        /* Clear state data */
        E.clear();
        E.shrink_to_fit();
        v.clear();
        v.shrink_to_fit();
        q.clear();
        q.shrink_to_fit();
        s.clear();
        s.shrink_to_fit();
        f_in.clear();
        f_in.shrink_to_fit();

        /* Clear recorded data, first sub arrays
           then top-level
         */
        out_signal.clear();
        out_signal.shrink_to_fit();
        rec_E.clear();
        rec_E.shrink_to_fit();
        rec_f_out.clear();
        rec_f_out.shrink_to_fit();
        rec_v.clear();
        rec_v.shrink_to_fit();
        rec_q.clear();
        rec_q.shrink_to_fit();
        rec_s.clear();
        rec_s.shrink_to_fit();
        rec_f_in.clear();
        rec_f_in.shrink_to_fit();
    }

    void record_targets() {} // nothing to do here ...

    std::vector< std::vector<%(float_prec)s> > out_signal;
    // record intermediate variables
    std::vector< std::vector<%(float_prec)s> > rec_E;
    std::vector< std::vector<%(float_prec)s> > rec_f_out;
    std::vector< std::vector<%(float_prec)s> > rec_v;
    std::vector< std::vector<%(float_prec)s> > rec_q;
    std::vector< std::vector<%(float_prec)s> > rec_s;
    std::vector< std::vector<%(float_prec)s> > rec_f_in;

    %(float_prec)s epsilon;
    %(float_prec)s alpha;
    %(float_prec)s kappa;
    %(float_prec)s gamma;
    %(float_prec)s E_0;
    %(float_prec)s V_0;
    %(float_prec)s tau_s;
    %(float_prec)s tau_f;
    %(float_prec)s tau_0;

private:
    %(float_prec)s k1_;
    %(float_prec)s k2_;
    %(float_prec)s k3_;

    std::vector<%(float_prec)s> E;
    std::vector<%(float_prec)s> v;
    std::vector<%(float_prec)s> q;
    std::vector<%(float_prec)s> s;
    std::vector<%(float_prec)s> f_in;
    std::vector<%(float_prec)s> f_out;
};
""",
            'pyx_struct': """

    # Population %(pop_id)s (%(pop_name)s) : Monitor
    cdef cppclass BoldMonitor%(pop_id)s (Monitor):
        BoldMonitor%(pop_id)s(vector[int], int, int, long) except +

        long int size_in_bytes()
        void clear()

        vector[vector[%(float_prec)s]] out_signal
        # record intermediate variables
        vector[vector[%(float_prec)s]] rec_E
        vector[vector[%(float_prec)s]] rec_f_out
        vector[vector[%(float_prec)s]] rec_v
        vector[vector[%(float_prec)s]] rec_q
        vector[vector[%(float_prec)s]] rec_s
        vector[vector[%(float_prec)s]] rec_f_in

        %(float_prec)s epsilon
        %(float_prec)s alpha
        %(float_prec)s kappa
        %(float_prec)s gamma
        %(float_prec)s E_0
        %(float_prec)s V_0
        %(float_prec)s tau_s
        %(float_prec)s tau_f
        %(float_prec)s tau_0

""",
            'pyx_wrapper': """

# Population Monitor wrapper
cdef class BoldMonitor%(pop_id)s_wrapper(Monitor_wrapper):
    def __cinit__(self, list ranks, int period, period_offset, long offset):
        self.thisptr = new BoldMonitor%(pop_id)s(ranks, period, period_offset, offset)

    def size_in_bytes(self):
        return (<BoldMonitor%(pop_id)s *>self.thisptr).size_in_bytes()

    def clear(self):
        (<BoldMonitor%(pop_id)s *>self.thisptr).clear()

    # Output
    property out_signal:
        def __get__(self): return (<BoldMonitor%(pop_id)s *>self.thisptr).out_signal

    # Intermediate Variables
    property E:
        def __get__(self): return (<BoldMonitor%(pop_id)s *>self.thisptr).rec_E
    property f_out:
        def __get__(self): return (<BoldMonitor%(pop_id)s *>self.thisptr).rec_f_out
    property v:
        def __get__(self): return (<BoldMonitor%(pop_id)s *>self.thisptr).rec_v
    property q:
        def __get__(self): return (<BoldMonitor%(pop_id)s *>self.thisptr).rec_q
    property s:
        def __get__(self): return (<BoldMonitor%(pop_id)s *>self.thisptr).rec_s
    property f_in:
        def __get__(self): return (<BoldMonitor%(pop_id)s *>self.thisptr).rec_f_in

    # Parameters
    property epsilon:
        def __set__(self, val): (<BoldMonitor%(pop_id)s *>self.thisptr).epsilon = val
    property alpha:
        def __set__(self, val): (<BoldMonitor%(pop_id)s *>self.thisptr).alpha = val
    property kappa:
        def __set__(self, val): (<BoldMonitor%(pop_id)s *>self.thisptr).kappa = val
    property gamma:
        def __set__(self, val): (<BoldMonitor%(pop_id)s *>self.thisptr).gamma = val
    property E_0:
        def __set__(self, val): (<BoldMonitor%(pop_id)s *>self.thisptr).E_0 = val
    property V_0:
        def __set__(self, val): (<BoldMonitor%(pop_id)s *>self.thisptr).V_0 = val
    property tau_s:
        def __set__(self, val): (<BoldMonitor%(pop_id)s *>self.thisptr).tau_s = val
    property tau_f:
        def __set__(self, val): (<BoldMonitor%(pop_id)s *>self.thisptr).tau_f = val
    property tau_0:
        def __set__(self, val): (<BoldMonitor%(pop_id)s *>self.thisptr).tau_0 = val

"""
        }

    #######################################
    ### Attributes
    #######################################
    # epsilon
    @property
    def epsilon(self):
        "TODO"
        if not self.cyInstance:
            return self._epsilon
        else:
            return self.cyInstance.epsilon
    @epsilon.setter
    def epsilon(self, val):
        if not self.cyInstance:
            self._epsilon = val
        else:
            self.cyInstance.epsilon = val
    # alpha
    @property
    def alpha(self):
        "TODO"
        if not self.cyInstance:
            return self._alpha
        else:
            return self.cyInstance.alpha
    @alpha.setter
    def alpha(self, val):
        if not self.cyInstance:
            self._alpha = val
        else:
            self.cyInstance.alpha = val
    # kappa
    @property
    def kappa(self):
        "TODO"
        if not self.cyInstance:
            return self._kappa
        else:
            return self.cyInstance.kappa
    @kappa.setter
    def kappa(self, val):
        if not self.cyInstance:
            self._kappa = val
        else:
            self.cyInstance.kappa = val
    # gamma
    @property
    def gamma(self):
        "TODO"
        if not self.cyInstance:
            return self._gamma
        else:
            return self.cyInstance.gamma
    @gamma.setter
    def gamma(self, val):
        if not self.cyInstance:
            self._gamma = val
        else:
            self.cyInstance.gamma = val
    # E_0
    @property
    def E_0(self):
        "TODO"
        if not self.cyInstance:
            return self._E_0
        else:
            return self.cyInstance.E_0
    @E_0.setter
    def E_0(self, val):
        if not self.cyInstance:
            self._E_0 = val
        else:
            self.cyInstance.E_0 = val
    # V_0
    @property
    def V_0(self):
        "TODO"
        if not self.cyInstance:
            return self._V_0
        else:
            return self.cyInstance.V_0
    @V_0.setter
    def V_0(self, val):
        if not self.cyInstance:
            self._V_0 = val
        else:
            self.cyInstance.V_0 = val
    # tau_s
    @property
    def tau_s(self):
        "TODO"
        if not self.cyInstance:
            return self._tau_s
        else:
            return self.cyInstance.tau_s
    @tau_s.setter
    def tau_s(self, val):
        if not self.cyInstance:
            self._tau_s = val
        else:
            self.cyInstance.tau_s = val
    # tau_f
    @property
    def tau_f(self):
        "TODO"
        if not self.cyInstance:
            return self._tau_f
        else:
            return self.cyInstance.tau_f
    @tau_f.setter
    def tau_f(self, val):
        if not self.cyInstance:
            self._tau_f = val
        else:
            self.cyInstance.tau_f = val
    # tau_0
    @property
    def tau_0(self):
        "TODO"
        if not self.cyInstance:
            return self._tau_0
        else:
            return self.cyInstance.tau_0
    @tau_0.setter
    def tau_0(self, val):
        if not self.cyInstance:
            self._tau_0 = val
        else:
            self.cyInstance.tau_0 = val

    # Intermediate Variables
    @property
    def E(self):
        return self.cyInstance.E

    @property
    def f_in(self):
        return self.cyInstance.f_in

    @property
    def f_out(self):
        return self.cyInstance.f_out

    @property
    def v(self):
        return self.cyInstance.v

    @property
    def q(self):
        return self.cyInstance.q

    @property
    def s(self):
        return self.cyInstance.s

    #######################################
    ### Data access
    #######################################
    def _start_bold_monitor(self):
        """
        Automatically called from Compiler._instantiate()
        """
        # Create the wrapper
        period = int(self._period/Global.config['dt'])
        period_offset = int(self._period_offset/Global.config['dt'])
        offset = Global.get_current_step(self.net_id) % period
        self.cyInstance = getattr(Global._network[self.net_id]['instance'], 'BoldMonitor'+str(self.object.id)+'_wrapper')(self.object.ranks, period, period_offset, offset)
        Global._network[self.net_id]['instance'].add_recorder(self.cyInstance)

        # Set the parameter
        self.cyInstance.epsilon = self._epsilon
        self.cyInstance.alpha = self._alpha
        self.cyInstance.kappa = self._kappa
        self.cyInstance.gamma = self._gamma
        self.cyInstance.E_0 = self._E_0
        self.cyInstance.V_0 = self._V_0
        self.cyInstance.tau_s = self._tau_s
        self.cyInstance.tau_f = self._tau_f
        self.cyInstance.tau_0 = self._tau_0

    def get(self, variables=None):
        """
        Get the recorded BOLD signal.
        """
        if variables == None:
            return self._get_population(self.object, "out_signal", True)
        else:
            raise ValueError
