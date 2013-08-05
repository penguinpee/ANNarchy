""" 
Generator.py
"""
import os, sys
import shutil

# ANNarchy core informations
import ANNarchy4.core.Global as Global

def create_includes():
    """
    generate 'Includes.h' containing all generated headers.
    """
    pop_header  = ''
    proj_header = ''

    for pop in Global.populations_:
        pop_header += '#include "'+pop.name+'.h"\n'

    proj_header = ''
    for proj in Global.generatedProj_:
        proj_header += '#include "'+ proj['name'] +'.h"\n'

    header = """#ifndef __ANNARCHY_INCLUDES_H__
#define __ANNARCHY_INCLUDES_H__

// population files
%(pop_header)s
// projection files
%(proj_header)s
#endif
""" % { 'pop_header': pop_header, 'proj_header': proj_header}

    with open(Global.annarchy_dir + '/build/Includes.h', mode = 'w') as w_file:
        w_file.write(header)

def update_annarchy_header(cpp_stand_alone):
    """
    update ANNarchy.h dependent on compilation mode (cpp_stand_alone):
        - True: instantiation of population, projection classes and projection instantiation.
        - False: only projection instantiation.
    """
    code = ''
    with open(Global.annarchy_dir+'/build/ANNarchy.h', mode = 'r') as r_file:
        for a_line in r_file:
            if a_line.find('//AddProjection') != -1:
                if(cpp_stand_alone):
                    for proj in Global.projections_:
                        code += proj.generate_cpp_add()
            elif a_line.find('//AddPopulation') != -1:
                if(cpp_stand_alone):
                    for pop in Global.populations_:
                        code += pop.generator.generate_cpp_add()
                        
            elif a_line.find('//createProjInstance') != -1:
                code += a_line
                code += generate_proj_instance_class()
            else:
                code += a_line

    with open(Global.annarchy_dir+'/build/ANNarchy.h', mode='w') as w_file:
        w_file.write(code)

def generate_proj_instance_class():
    """
    The standard ANNarchy core has no knowledge about the full amount of projection
    classes. On the other hand we want to instantiate the object from there. To achieve this
    we introduce a projection instantiation class, which returns a projections instance corresponding
    to the given ID.
    """
    # single cases
    cases = ''
    for proj in Global.generatedProj_:
        cases += """
        case %(id)s:
            return new %(name)s(pre, post, postNeuronRank, target);

""" % { 'id': proj['ID'], 'name': proj['name']}

    # complete code
    code = """class createProjInstance {
public:
    createProjInstance() {};

    Projection* getInstanceOf(int ID, Population *pre, Population *post, int postNeuronRank, int target) {
        switch(ID) {
            case 0:
                return new Projection(pre, post, postNeuronRank, target);
%(case)s
            default:
                std::cout << "Unknown typeID" << std::endl;
                return NULL;
        }
    }
};
""" % { 'case': cases }
    return code

def generate_py_extension():
    """
    Hence the amount of code is higher, we decide to split up the code. Nevertheless cython generates 
    one shared library per .pyx file. To retrieve only one library we need to compile only one .pyx file
    which includes all the others. 
    """
    pop_include = ''
    for pop in Global.populations_:
        pop_include += 'include \"'+pop.name+'.pyx\"\n'

    code = """include "Network.pyx"
include "Simulation.pyx"
include "Projection.pyx"
include "Connector.pyx"
%(inc)s    
""" % { 'inc': pop_include }

    with open(Global.annarchy_dir+'/pyx/ANNarchyCython.pyx', mode='w') as w_file:
        w_file.write(code)
        
def folder_management():
    """
    ANNarchy is provided as a python package. For compilation a local folder
    'annarchy' is created in the current working directory.
    """
    if os.path.exists(Global.annarchy_dir):
        shutil.rmtree(Global.annarchy_dir, True)
    
    os.mkdir(Global.annarchy_dir)
    os.mkdir(Global.annarchy_dir+'/pyx')
    os.mkdir(Global.annarchy_dir+'/build')

    sources_dir = os.path.abspath(os.path.dirname(__file__)+'/../data')

    for file in os.listdir(sources_dir):
        if not os.path.isdir(os.path.abspath(sources_dir+'/'+file)):
            shutil.copy(sources_dir+'/'+file, Global.annarchy_dir)
            
    for file in os.listdir(sources_dir+'/cpp'):
        shutil.copy(sources_dir+'/cpp/'+file, # src
                    Global.annarchy_dir+'/build/'+file # dest
                    )
        
    for file in os.listdir(sources_dir+'/pyx'):
        shutil.copy(sources_dir+'/pyx/'+file, #src
                    Global.annarchy_dir+'/pyx/'+file #dest
                    )

    sys.path.append(Global.annarchy_dir)

def code_generation(cpp_stand_alone):
    """
    code generation for each population respectively projection object the user defined. 
    
    After this the ANNarchy main header is expanded by the corresponding headers.
    """
    print '\nGenerate files\n'
    for pop in Global.populations_:
        pop.generator.generate()

    for proj in Global.projections_:
        proj.generate()

    create_includes()

    update_annarchy_header(cpp_stand_alone)

    generate_py_extension()
    
def compile(cpp_stand_alone=False, debug_build=False):
    """
    compilation consists of 3 steps:
    
        a) generate user defined classes and cython wrapper
        b) compile ANNarchyCore
        c) compile ANNarchyCython
        
    after this we instantiate the cythonized objects. 
    """
    print Global.version, 'on', os.name
    
    folder_management()
    
    code_generation(cpp_stand_alone)
    
    #
    # create ANNarchyCore.so and py extensions
    print '\nStart compilation ...\n'
    if sys.platform.startswith('linux'):
        import subprocess
        os.chdir(Global.annarchy_dir)

        #
        # apply +x lost by copy
        os.system('chmod +x compile*')

        if not debug_build:
            proc = subprocess.Popen(['./compile.sh'])
            proc.wait()
        else:
            proc = subprocess.Popen(['./compiled.sh'])
            proc.wait()
        
        os.chdir('..')

        #
        # bind the py extensions to the corresponding python objects
        import ANNarchyCython
        for pop in Global.populations_:
            pop.cyInstance = eval('ANNarchyCython.py'+
                                  pop.name.capitalize()+'()')

        #
        # instantiate projections
        for proj in Global.projections_:
            conn = proj.connector.init_connector()          
            proj.cyInstance = conn.connect(proj.pre,
                                        proj.post,
                                        proj.connector.weights,
                                        proj.post.generator.targets.index(proj.target),
                                        proj.connector.parameters
                                        )

    else:
        error = """automated compilation and cython/python binding 
        only available under linux currently."""
        print error

    print '\nCompilation process done.\n'
    
def simulate(duration):
    """
    simulate #duration steps
    """    
    import ANNarchyCython
    ANNarchyCython.pyNetwork().Run(duration)
    
