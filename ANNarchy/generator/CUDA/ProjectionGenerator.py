import ANNarchy.core.Global as Global

import numpy as np

class ProjectionGenerator(object):
    
    def header_struct(self, proj):    
        # Is it a specific projection?
        if proj.generator['cuda']['header_proj_struct']:
            return proj.generator['cuda']['header_proj_struct']

        code = """
struct ProjStruct%(id)s{
    int size;

    // stream
    cudaStream_t stream;
    
    // Learning flag
    bool _learning;
    // Connectivity
    std::vector<int> post_rank ;
    int* gpu_post_rank;
    std::vector< std::vector< int > > pre_rank ;
    int* gpu_pre_rank;
    int* gpu_nb_synapses;
    int* gpu_off_synapses;
    
    // flat connectivity parameters 
    int overallSynapses;
    std::vector<int> flat_idx;
    std::vector<int> flat_off;
"""

        # Delays
        if proj.max_delay > 1 and proj._synapses.uniform_delay == -1:
            if proj._synapses.type == "rate":
                Global._error("only uniform delays are supported ...")
                exit(0)

        # Arrays for the random numbers
        code += """
    // RNG states
"""
        for rd in proj.synapse.description['random_distributions']:
            code += """    curandState* gpu_%(rd_name)s;
""" % { 'rd_name' : rd['name'] }

        # Parameters
        for var in proj.synapse.description['parameters']:
            if var['name'] in proj.synapse.description['local']:
                code += """
    // Local parameter %(name)s
    std::vector< std::vector< %(type)s > > %(name)s;    // host
    %(type)s* gpu_%(name)s;    // device
    bool %(name)s_dirty;    
""" % {'type' : var['ctype'], 'name': var['name']}
            elif var['name'] in proj.synapse.description['global']:
                code += """
    // Global parameter %(name)s
    std::vector<%(type)s>  %(name)s;
    %(type)s* gpu_%(name)s;    // device
    bool %(name)s_dirty;
""" % {'type' : var['ctype'], 'name': var['name']}

        # Variables
        for var in proj.synapse.description['variables']:
            if var['name'] in proj.synapse.description['local']:
                code += """
    // Local variable %(name)s
    std::vector< std::vector< %(type)s > > %(name)s ;    // host
    %(type)s* gpu_%(name)s;    // device
    bool %(name)s_dirty;
    // std::vector< std::vector< %(type)s > > recorded_%(name)s ;
    // bool record_%(name)s ;
""" % {'type' : var['ctype'], 'name': var['name']}
            elif var['name'] in proj.synapse.description['global']:
                code += """
    // Global variable %(name)s
    std::vector<%(type)s>  %(name)s;    // host
    %(type)s* gpu_%(name)s;    // device
    bool %(name)s_dirty;
    // std::vector< %(type)s > recorded_%(name)s ;
    // bool record_%(name)s ;
""" % {'type' : var['ctype'], 'name': var['name']}

        # Pre- or post_spike variables (including w)
        if proj.synapse.description['type'] == 'spike':
            for var in proj.synapse.description['pre_spike']:
                if not var['name'] in proj.synapse.description['attributes'] + ['g_target']:
                    code += """
    // Local variable %(name)s added by default
    std::vector< std::vector< %(type)s > > %(name)s ;
    // std::vector< std::vector< %(type)s > > recorded_%(name)s ;
    // bool record_%(name)s ;
""" % {'type' : 'double', 'name': var['name']}

        code += """
};    
""" 
        return code % {'id': proj.id}


    def computesum_rate(self, proj):
        """
        returns all data needed for compute postsynaptic sum kernels:

        header:  kernel prototypes
        body:    kernel implementation
        call:    kernel call
        """
        # Is it a specific projection?
        if proj.generator['cuda']['body_compute_psp']:
            Global._error("Customized rate-code projections are not usable on CUDA yet.")
            return "", "", ""

        # Retrieve the psp code
        if not 'psp' in  proj.synapse.description.keys(): # default
            psp = "r[pre_rank[i]] * w[i];"
        else: # custom psp
            psp = proj.synapse.description['psp']['cpp'] % {'id_proj' : proj.id, 'id_post': proj.post.id, 'id_pre': proj.pre.id}

        from .cuBodyTemplate import psp_kernel
        body_code = psp_kernel % { 'id': proj.id,
                                   'pre': proj.pre.id,
                                   'post': proj.post.id,
                                   'target': proj.target,
                                   'psp': psp
                                  }

        header_code = """void Pop%(pre)s_Pop%(post)s_%(target)s_psp( cudaStream_t stream, int size, int* pre_rank, int* nb_synapses, int *offsets, double *r, double* w, double *sum_%(target)s );
""" % { 'id': proj.id,
        'pre': proj.pre.id,
        'post': proj.post.id,
        'target': proj.target,
      }

        from .cuBodyTemplate import psp_kernel_call
        call_code = psp_kernel_call % { 'id': proj.id,
                                        'pre': proj.pre.id,
                                        'post': proj.post.id,
                                        'target': proj.target,
                                      }

        # Take delays into account if any
        if proj.max_delay > 1:
            if proj.uniform_delay == -1:
                Global._error("only uniform delays are supported on GPUs.")
                exit(0)
            else:
                call_code = call_code.replace("gpu_r", "gpu_delayed_r["+str(proj.max_delay-1)+"]")

        return body_code, header_code, call_code

    def computesum_spiking(self, proj):
        # Is it a specific projection?
        if proj.generator['cuda']['body_compute_psp']:
            Global._error("Customized spiking projections are not usable on CUDA yet.")
            return "", "", ""

        Global._error("Spiking models are not supported currently on CUDA devices.")
        return "", "", ""

    def update_synapse(self, proj):
        from ..Utils import generate_equation_code

        # Global variables
        global_eq = generate_equation_code(proj.id, proj.synapse.description, 'global', 'proj') %{'id_proj' : proj.id, 'target': proj.target, 'id_post': proj.post.id, 'id_pre': proj.pre.id}

        # Local variables
        local_eq =  generate_equation_code(proj.id, proj.synapse.description, 'local', 'proj') %{'id_proj' : proj.id, 'target': proj.target, 'id_post': proj.post.id, 'id_pre': proj.pre.id}  

        if global_eq.strip() == '' and local_eq.strip() == '':
            return "", "", ""

        # pre- and postsynaptic global operations
        pre_global_ops = []
        for pre_glob in proj.synapse.description['pre_global_operations']:
            pre_global_ops.append( """_%(func)s_%(name)s""" % { 'func': pre_glob['function'], 'name': pre_glob['variable'] } )

        post_global_ops = []
        for post_glob in proj.synapse.description['post_global_operations']:
            post_global_ops.append( """_%(func)s_%(name)s""" % { 'func': post_glob['function'], 'name': post_glob['variable'] } )

        # remove doubled entries
        pre_dependencies = list(set(proj.synapse.description['dependencies']['pre']))
        pre_global_ops = list(set(pre_global_ops))
        post_global_ops = list(set(post_global_ops))
        post_dependencies = list(set(proj.synapse.description['dependencies']['post']))

        # remove unnecessary stuff, transfrom index of OMP to CUDA
        local_eq = local_eq.replace("proj"+str(proj.id)+".","")
        local_eq = local_eq.replace("[i][j]","[j]")

        # remove unnecessary stuff
        global_eq = global_eq.replace("proj"+str(proj.id)+".","")

        var = ""
        par = ""
        # synaptic variables / parameters
        for attr in proj.synapse.description['variables'] + proj.synapse.description['parameters']:
            var += """, %(type)s* %(name)s """ % { 'type': attr['ctype'], 'name': attr['name'] }

        # replace pre- and postsynaptic global operations / variable accesses
        for pre_var in pre_dependencies:
            old = """pop%(id)s.%(name)s""" % { 'id': proj.pre.id, 'name': pre_var}
            new = """pre_%(name)s""" % { 'name': pre_var}
            var += ", double* " + new
            local_eq = local_eq.replace(old, new)
            global_eq = global_eq.replace(old, new)
        for g_op in pre_global_ops:
            old = """pop%(id)s.%(name)s""" % { 'id': proj.pre.id, 'name': g_op}
            new = """pre_%(name)s""" % { 'name': g_op}
            par += ", double " + new
            local_eq = local_eq.replace(old, new)
            global_eq = global_eq.replace(old, new)
        for post_var in post_dependencies:
            old = """pop%(id)s.%(name)s""" % { 'id': proj.post.id, 'name': post_var}
            new = """post_%(name)s""" % { 'name': post_var}
            var += ", double* " + new
            local_eq = local_eq.replace(old, new)
            global_eq = global_eq.replace(old, new)
        for g_op in post_global_ops:
            old = """pop%(id)s.%(name)s""" % { 'id': proj.post.id, 'name': g_op}
            new = """post_%(name)s""" % { 'name': g_op}
            par += ", double " + new
            local_eq = local_eq.replace(old, new)
            global_eq = global_eq.replace(old, new)

        # random variables
        for rd in proj.synapse.description['random_distributions']:
            par += """, curandState* %(rd_name)s""" % { 'rd_name' : rd['name'] }

        # we replace the rand_%(id)s by the corresponding curand... term
        for rd in proj.synapse.description['random_distributions']:
            if rd['dist'] == "Uniform":
                term = """curand_uniform_double( &%(rd)s[i]) * (%(max)s - %(min)s) + %(min)s""" % { 'rd': rd['name'], 'min': rd['args'].split(',')[0], 'max': rd['args'].split(',')[1] };
                local_eq = local_eq.replace(rd['name']+"[j]", term)
            elif rd['dist'] == "Normal":
                term = """curand_normal_double( &%(rd)s[i])""" % { 'rd': rd['name'] };
                local_eq = local_eq.replace(rd['name']+"[j]", term)
            elif rd['dist'] == "LogNormal":
                term = """curand_log_normal_double( &%(rd)s[i], %(mean)s, %(std_dev)s)""" % { 'rd': rd['name'], 'mean': rd['args'].split(',')[0], 'std_dev': rd['args'].split(',')[1] };
                local_eq = local_eq.replace(rd['name']+"[j]", term)
            else:
                Global._error("Unsupported random distribution on GPUs: " + rd['dist'])

        # remove all types
        repl_types = ["double*", "float*", "int*", "curandState*", "double", "float", "int"]
        var_wo_types = var
        par_wo_types = par
        for type in repl_types:
            var_wo_types = var_wo_types.replace(type, "")
            par_wo_types = par_wo_types.replace(type, "")

        from .cuBodyTemplate import syn_kernel
        body = syn_kernel % { 'id': proj.id,
                               'par': par,
                               'par2': par_wo_types,
                               'var': var,
                               'var2': var_wo_types,
                               'global_eqs': global_eq,
                               'local_eqs': local_eq,
                               'target': proj.target,
                               'pre': proj.pre.id,
                               'post': proj.post.id,
                             }

        header = """void Proj%(id)s_step(cudaStream_t stream, int size, int* post_rank, int *pre_rank, int *offsets, int *nb_synapses, double dt%(var)s%(par)s);
    """ % { 'id': proj.id,
            'var': var,
            'par': par
          }

        #
        # calling entity
        local = ""
        for attr in proj.synapse.description['variables'] + proj.synapse.description['parameters']:
            local += """, proj%(id)s.gpu_%(name)s """ % { 'id': proj.id, 'name': attr['name'] }

        for pre_var in pre_dependencies:
            local += """, pop%(id)s.gpu_%(name)s """ % { 'id': proj.pre.id, 'name': pre_var }

        for post_var in post_dependencies:
            local += """, pop%(id)s.gpu_%(name)s """ % { 'id': proj.post.id, 'name': post_var }

        glob = ""
        for g_op in pre_global_ops:
            glob += """, pop%(id)s.%(name)s """ % { 'id': proj.pre.id, 'name': g_op }
        for g_op in post_global_ops:
            glob += """, pop%(id)s.%(name)s """ % { 'id': proj.post.id, 'name': g_op }

        # random variables
        for rd in proj.synapse.description['random_distributions']:
            glob += """, proj%(id)s.gpu_%(rd_name)s""" % { 'id': proj.id, 'rd_name' : rd['name'] }

        # generate code
        from .cuBodyTemplate import syn_kernel_call
        call = syn_kernel_call % { 'id': proj.id,
                                   'post': proj.post.id,
                                   'pre': proj.pre.id,
                                   'local': local,
                                   'glob': glob
                                 }

        return body, header, call

    def pruning(self, proj):
        Global._error("Pruning is not implemented for CUDA ... ")
        return ""

    def init_random_distributions(self, proj):
        # Is it a specific projection?
        if proj.generator['omp']['body_random_dist_init']:
            return proj.generator['omp']['body_random_dist_init'] %{'id_proj': proj.id}

        code = ""
        for rd in proj.synapse.description['random_distributions']:
            code += """    cudaMalloc((void**)&proj%(id)s.gpu_%(rd_name)s, pop%(post)s.size * sizeof(curandState));
    init_curand_states( pop%(post)s.size, proj%(id)s.gpu_%(rd_name)s, seed );
""" % {'id': proj.id, 'post': proj.post.id, 'rd_name': rd['name'] }

        return code

    def init_projection(self, proj):
        code = ""
        # Is it a specific projection?
        if proj.generator['cuda']['body_proj_init']:
            return proj.generator['cuda']['body_proj_init']

        # Learning by default
        code += """
    // proj%(id_proj)s: %(name_pre)s -> %(name_post)s with target %(target)s
    proj%(id_proj)s._learning = true;
""" % {'id_proj': proj.id, 'target': proj.target, 'id_post': proj.post.id, 'id_pre': proj.pre.id, 'name_post': proj.post.name, 'name_pre': proj.pre.name}

        # Spiking neurons have aditional data
        if proj.synapse.type == 'spike':
            Global._error("no spiking implementation yet ..")

        # Recording
        # TODO: not implemented yet

        return code

    def record(self, proj):
        # TODO: not implemented yet
        return ""
