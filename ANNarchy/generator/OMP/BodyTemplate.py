body_template = '''
#include "ANNarchy.h"

/*
 * Internal data
 *
*/
double dt;
long int t;
std::vector< std::mt19937 >  rng;

// Populations
%(pop_ptr)s

// Projections
%(proj_ptr)s

// Global operations
%(glops_def)s

// Simulate the network for the given number of steps
void run(int nbSteps) {

    for(int i=0; i<nbSteps; i++)
    {
        step();
    }

}

// Initialize the internal data and random numbers generators
void initialize(double _dt) {

    // Internal variables
    dt = _dt;
    t = (long int)(0);

    // Random number generators
    int threads = std::max(1, omp_get_max_threads());
    for(int seed = 0; seed < threads; ++seed)
    {
        rng.push_back(std::mt19937(time(NULL)*seed));
    }
%(random_dist_init)s
%(delay_init)s
%(spike_init)s
%(projection_init)s
%(globalops_init)s
}

// Step method. Generated by ANNarchy.
void step()
{

    ////////////////////////////////
    // Presynaptic events
    ////////////////////////////////
    double sum;
%(compute_sums)s

    ////////////////////////////////
    // Reset spikes
    ////////////////////////////////


    ////////////////////////////////
    // Update random distributions
    ////////////////////////////////
%(random_dist_update)s

    ////////////////////////////////
    // Update neural variables
    ////////////////////////////////
%(update_neuron)s    

    ////////////////////////////////
    // Delay outputs
    ////////////////////////////////
%(delay_code)s

    ////////////////////////////////
    // Global operations (min/max/mean)
    ////////////////////////////////
%(update_globalops)s    


    ////////////////////////////////
    // Update synaptic variables
    ////////////////////////////////
    int rk_pre, rk_post;
%(update_synapse)s    


    ////////////////////////////////
    // Postsynaptic events
    ////////////////////////////////
%(post_event)s

    ////////////////////////////////
    // Recording
    ////////////////////////////////
%(record)s

    ////////////////////////////////
    // Increase internal time
    ////////////////////////////////
    t++;
}


/*
 * Access to time and dt
 *
*/
long int getTime() {return t;}
void setTime(long int t_) { t=t_;}
double getDt() { return dt;}
void setDt(double dt_) { dt=dt_;}

/*
 * Number of threads
 *
*/
void setNumThreads(int threads)
{
    omp_set_num_threads(threads);
}
'''