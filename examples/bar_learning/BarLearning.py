#
#   BarLearning example for ANNarchy4
#
#   authors: Julien Vitay, Helge Uelo Dinkelbach
#
from ANNarchy4 import *

# Defining the neurons
InputNeuron = RateNeuron(
    parameters=""" 
        tau = 10.0 : population
        baseline = 0.0 
    """,
    equations="""
        tau * drate/dt + rate = baseline : min=0.0
    """
)

LeakyNeuron = RateNeuron(
    parameters=""" 
        tau = 10.0 : population
        baseline = 0.0 
    """,
    equations="""
        tau * drate/dt + rate = sum(exc) - sum(inh) : min=0.0
    """
)

# Defining the synapses
Oja = RateSynapse(
    parameters=""" 
        tau = 2000 : postsynaptic
        alpha = 8.0 : postsynaptic
    """,
    equations="""
        tau * dvalue/dt = pre.rate * post.rate - alpha * post.rate^2 * value
    """
)  

AntiHebb = RateSynapse(
    parameters=""" 
        tau = 2000 : postsynaptic
        alpha = 0.3 : postsynaptic
    """,
    equations="""
        tau * dvalue/dt = pre.rate * post.rate - alpha * post.rate^2 * value : min = 0.0
    """
)  

# Creating the populations
nb_neurons = 128  
input_pop = Population(geometry=(nb_neurons, nb_neurons), neuron=InputNeuron)
feature_pop = Population(geometry=(nb_neurons, 4), neuron=LeakyNeuron)

# Creating the projections
input_feature = Projection(
    pre=input_pop, 
    post=feature_pop, 
    target='exc', 
    synapse = Oja,
    connector=All2All(weights = Uniform(-0.5, 0.5))
)
                     
feature_feature = Projection(
    pre=feature_pop, 
    post=feature_pop, 
    target='inh', 
    synapse = AntiHebb,
    connector=All2All(weights = Uniform(0.0, 1.0))
) 

# Definition of the environment
def set_input():
    # Choose which bars will be used as inputs
    values = np.zeros((nb_neurons, nb_neurons))
    for w in range(nb_neurons):
        if np.random.random() < 1./ float(nb_neurons):
            values[:, w] = 1.
    for h in range(nb_neurons):
        if np.random.random() < 1./ float(nb_neurons):
            values[h, :] = 1.

    # Set the input
    input_pop.baseline = values.reshape(nb_neurons**2)

def setup_visualize():
    # Collect visualizing information
    plot1 = {'pop': input_pop, 'var': 'rate'}
    plot2 = {'pop': feature_pop, 'var': 'rate'}
    plot3 = {'proj': input_feature, 'var': 'value', 
         'max': 0.1, 'title': 'Receptive fields'}

    # Setup visualizer
    vis = Visualization( [plot1, plot2, plot3 ] )

# visualization meanwhile yes/no
vis_during_sim=True

def simulate_sth():
    # Run the simulation        
    for trial in range(3000):
        set_input()
        net.simulate(50) 
        
        if vis_during_sim:
           vis.render()

    # Visualize the result of learning
    vis.render()  

    print 'simulation finished.'

if __name__=='__main__':

    # Compiling the network
    compile(cpp_stand_alone=True)

    setup_visualize()

    profiler = Profile()

    #
    # setup the test
    num_trials = 10
    thread_count = [6,4,2,1]
    trial_dur = 50

    #
    # pre setup
    diff_runs = []
    index = [ x for x in xrange(num_trials) ]

    for test in range(len(thread_count)):
        diff_runs.append( [0 for x in range(num_trials) ] )

        profiler.set_num_threads(thread_count[test])   

        simulate_sth()

    print 'all simulation finished.'

    raw_input()
