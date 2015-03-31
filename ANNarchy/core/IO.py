"""

    IO.py
    
    This file is part of ANNarchy.
    
    Copyright (C) 2013-2016  Julien Vitay <julien.vitay@gmail.com>,
    Helge Uelo Dinkelbach <helge.dinkelbach@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ANNarchy is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
"""
from ANNarchy.core import Global 
import os
import cPickle

def load_parameter(in_file):
    """
    Load parameter set from xml file.
    
    Parameters:
    
    * *in_file*: either single or collection of strings. if the location of the xml file differs from the base directory, you need to provide relative or absolute path.
    """
    try:
        from lxml import etree 
    except:
        Global._print('lxml is not installed. Unable to save in xml format.')
        return
    par = {}
    damaged_pars = []   # for printout
    
    files = []
    if isinstance(in_file,str):
        files.append(in_file)
    else:
        files = in_file
    
    for file in files:
        try:
            doc = etree.parse(file)
            
        except IOError:
            print('Error: file \'',file,'\' not found.')
            continue
        
        matches = doc.findall('parameter')
        
        for parameter in matches:
            childs = parameter.getchildren()
    
            #TODO: allways correct ???
            if len(childs) != 2:
                print('Error: to much tags in parameter')
    
            name=None
            value=None
            for child in childs:
    
                if child.tag == 'name':
                    name = child.text
                elif child.tag == 'value':
                    value = child.text
                    
                    if value == None:
                        print('Error: no value defined for',name)
                        damaged_pars.append(name)
                        value = 0
                    else:
                        try:
                            value = int(value)
                        except ValueError:
                            try:
                                value = float(value)
                            except ValueError:
                                value = value
                        
                else:
                    print('Error: unexpected xml-tag', child.tag)
            
            if name == None:
                print('Error: no name in parameter set.')
            elif value == None:
                print('Error: no value in parameter set.')
                damaged_pars.append(name)
            elif name in par.keys():
                print("Error: parameter",name,"already exists.")
                damaged_pars.append(name)
            else:
                par[name] = value
             
    return par
    
def _save_data(filename, data):
    """
    Internal routine to save data in a file.
    
    """    
    # Check if the repertory exist
    (path, fname) = os.path.split(filename) 
    
    if not path == '':
        if not os.path.isdir(path):
            print('creating folder', path)
            os.mkdir(path)
    
    extension = os.path.splitext(fname)[1]
    
    if extension == '.mat':
        Global._debug("Save in Matlab format.")
        import scipy.io as sio
        sio.savemat(filename, data)
        
    elif extension == '.gz':
        Global._debug("Save in gunzipped binary format.")
        try:
            import gzip
        except:
            Global._error('gzip is not installed.')
            return
        with gzip.open(filename, mode = 'wb') as w_file:
            try:
                cPickle.dump(data, w_file, protocol=cPickle.HIGHEST_PROTOCOL)
            except Exception as e:
                print('Error while saving in gzipped binary format.')
                print(e)
                return
        
    else:
        Global._debug("Save in text format.")
        # save in Pythons pickle format
        with open(filename, mode = 'w') as w_file:
            try:
                cPickle.dump(data, w_file, protocol=cPickle.HIGHEST_PROTOCOL)
            except Exception as e:
                print('Error while saving in text format.')
                print(e)
                return
        return
    
def save(filename, populations=True, projections=True):#, pure_data=True):
    """
    Save the current network state to a file.

    * If the extension is '.mat', the data will be saved as a Matlab 7.2 file. Scipy must be installed.

    * If the extension ends with '.gz', the data will be pickled into a binary file and compressed using gzip.

    * Otherwise, the data will be pickled into a simple binary text file using cPickle.
    
    Parameter:
    
    * *filename*: filename, may contain relative or absolute path.
    
    * *populations*: if True, population data will be saved (by default True)
    
    * *projections*: if True, projection data will be saved (by default True)

    .. warning:: 

        The '.mat' data will not be loadable by ANNarchy, it is only for external analysis purpose. 
    
    Example::
        
        save('results/init.data')
    
        save('results/init.txt.gz')
        
        save('1000_trials.mat')
    
    """        
    data = _net_description(populations, projections)
    _save_data(filename, data)

def _load_data(filename):
    " Internally loads data contained in a file"   

    (path, fname) = os.path.split(filename)
    extension = os.path.splitext(fname)[1]
    desc = None
    if extension == '.mat':
        Global._error('Unable to load Matlab format.')
        return desc
    elif extension == '.gz':
        try:
            import gzip
        except:
            Global._error('gzip is not installed.')
            return desc
        try:
            with gzip.open(filename, mode = 'rb') as r_file:
                desc = cPickle.load(r_file)
        except Exception as e:
            print('Unable to read the file ' + filename)
            print(e)
            return desc

    else:
        try:
            with open(filename, mode = 'r') as r_file:
                desc = cPickle.load(r_file)
        except Exception as e:
            print('Unable to read the file ' + filename)
            print(e)
            return desc
    return desc

def load(filename, populations=True, projections=True):#, pure_data=True): TODO
    """
    Loads a saved state of the network.

    Warning: Matlab data can not be loaded.
    
    *Parameters*:
    
    * **filename**: the filename with relative or absolute path.
    
    * **populations**: if True, population data will be loaded (by default True)
    
    * **projections**: if True, projection data will be loaded (by default True)
    
    Example::
    
        load('results/network.data')
            
    """   

    desc = _load_data(filename)
    if desc == None:
        return
    if populations:
        # Over all populations
        for pop in Global._populations:  
            # check if the population is contained in save file
            if pop.name in desc.keys():
                _load_pop_data(pop, desc[pop.name])  
    if projections:    
        for proj in Global._projections : 
            if proj.name in desc.keys():            
                _load_proj_data(proj, desc[proj.name])

  
def _net_description(populations, projections):
    """
    Returns a dictionary containing the requested network data.
    
    Parameter:
    
        * *populations*: if *True* the population data will be saved
        * *projections*: if *True* the projection data will be saved
    """
    network_desc = {}   
    
    if populations:
        for pop in Global._populations:             
            network_desc[pop.name] = pop._data() 

    if projections:
        for proj in Global._projections:  
            network_desc[proj.name] = proj._data() 


    return network_desc
            
def _load_pop_data(pop, desc):
    """
    Update a population with the stored data set. 
    """
    if not 'attributes' in desc.keys():
        _error('Saved with a too old version of ANNarchy (< 4.2).')
        return
    for var in desc['attributes']:
        try:
            getattr(pop.cyInstance, 'set_'+var)(desc[var]) 
        except:
            Global._error('Can not load the variable ' + var + ' in the population ' + pop.name)
            return

    
def _load_proj_data(proj, desc):
    """
    Update a projection with the stored data set. 
    """       
    if not desc['post_ranks'] == proj.post_ranks:
        Global._error('The current projection has not the same number of postsynaptic neurons as in the saved file.')
        return
    if not 'attributes' in desc.keys():
        _error('Saved with a too old version of ANNarchy (< 4.2).')
        return
    for dendrite in desc['dendrites']:
        rk = dendrite['post_rank']
        for var in desc['attributes']:
            if var in ['rank', 'delay']:
                continue
            try:
                getattr(proj.cyInstance, 'set_dendrite_' + var)(rk, dendrite[var])
            except Exception, e:
                Global._print(e)
                Global._error('Can not set attribute ' + var + ' in the projection.')
                return

