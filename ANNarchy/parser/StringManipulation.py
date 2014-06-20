"""

    StringManipulation.py

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
####################################
# Functions for string manipulation
####################################
import re
from ANNarchy.core.Global import _error, _warning, authorized_keywords
        
def split_equation(definition):
    " Splits a description into equation and flags."
    try:
        equation, constraint = definition.rsplit(':', 1)
    except ValueError:
        equation = definition.strip() # there are no constraints
        constraint = None
    else:
        has_constraint = False
        for keyword in authorized_keywords:
            if keyword in constraint:
                has_constraint = True
        if has_constraint:
            equation = equation.strip()
            constraint = constraint.strip()
        else:
            equation = definition.strip() # there are no constraints
            constraint = None            
    finally:
        return equation, constraint
    
def prepare_string(stream):
    """ Splits up a multiline equation, remove comments and unneeded spaces or tabs."""
    expr_set = []        
    # replace the ,,, by empty space and split the result up
    tmp_set = re.sub('\s+\.\.\.\s+', ' ', stream).split('\n')
    for expr in tmp_set:
        expr = re.sub('\#[\s\S]+', ' ', expr)   # remove comments
        expr = re.sub('\s+', ' ', expr)     # remove additional tabs etc.
        if expr.strip() == '' or len(expr)==0: # through beginning line breaks or something similar empty strings are contained in the set
            continue           
        expr_set.append(''.join(expr))        
    return expr_set 

def extract_name(equation, left=False):
    " Extracts the name of a parameter/variable by looking the left term of an equation."
    equation = equation.replace(' ','')
    if not left: # there is potentially an equal sign
        try:
            name = equation.split('=')[0]
        except: # No equal sign. Eg: baseline : init=0.0
            return equation.strip()
        
        # Search for increments
        operators = ['+=', '-=', '*=', '/=', '>=', '<=']
        for op in operators:
            if op in equation: 
                return equation.split(op)[0]  
    else:
        name = equation.strip()          
        # Search for increments
        operators = ['+', '-', '*', '/']
        for op in operators:
            if equation.endswith(op): 
                return equation.split(op)[0]      
    # Search for any operation in the left side
    operators = ['+', '-', '*', '/']
    ode = False
    for op in operators:
        if not name.find(op) == -1: 
            ode = True
    if not ode: # variable name is alone on the left side
        return name
    # ODE: the variable name is between d and /dt
    name = re.findall("d([\w]+)/dt", name)
    if len(name) == 1:
        return name[0].strip()
    else:
        return '_undefined' 

def extract_condition_name(equation):
    " Extracts the name of a parameter/variable by looking the left term of an equation."
    # Search for operators
    operators = ['>', '<', '!=', '==', ' is ']
    for op in operators:
        if op in equation: 
            return equation.split(op)[0].strip()
    return '_undefined'   
    
                
def extract_flags(constraint):
    """ Extracts from all attributes given after : which are bounds (eg min=0.0 or init=0.1) 
        and which are flags (eg postsynaptic, implicit...).
    """
    bounds = {}
    flags = []
    # Check if there are constraints at all
    if not constraint:
        return bounds, flags
    # Split according to ','
    for con in constraint.split(','):
        try: # bound of the form key = val
            key, value = con.split('=')
            bounds[key.strip()] = value.strip()
        except ValueError: # No equal sign = flag
            flags.append(con.strip())
    return bounds, flags     
        
def process_equations(equations):
    """ Takes a multi-string describing equations and returns a list of dictionaries, where:
    
    * 'name' is the name of the variable
    
    * 'eq' is the equation
    
    * 'constraints' is all the constraints given after the last :. _extract_flags() should be called on it.
    
    Warning: one equation can now be on multiple lines, without needing the ... newline symbol.
    
    TODO: should this be used for other arguments as equations? pre_event and so on
    """
    def is_constraint(eq):
        " Internal method to determine if a string contains reserved keywords." 
        eq = ',' +  eq.replace(' ', '') + ','
        for key in authorized_keywords:
            pattern = '([,]+)' + key + '([=,]+)'
            if re.match(pattern, eq):
                return True
        return False
    # All equations will be stored there, in the order of their definition
    variables = []        
    
    # Iterate over all lines
    for line in equations.splitlines():
        # Skip empty lines
        definition = line.strip()
        if definition == '':
            continue
        # Remove comments
        com = definition.split('#')
        if len(com) > 1:
            definition = com[0]
            if definition.strip() == '':
                continue
        # Process the line
        try:
            equation, constraint = definition.rsplit(':', 1)
        except ValueError: # There is no :, only equation is concerned 
            equation = line
            constraint = ''
        else:   # there is a :
            # Check if the constraint contains the reserved keywords
            has_constraint = is_constraint(constraint)
            # If the right part of : is a constraint, just store it
            # Otherwise, it is an if-then-else statement
            if has_constraint:
                equation = equation.strip()
                constraint = constraint.strip()
            else:
                equation = definition.strip() # there are no constraints
                constraint = '' 
        # Split the equation around operators = += -= *= /=, but not ==
        split_operators = re.findall('([\s\w\+\-\*\/]+)=([^=])', equation)
        if len(split_operators) == 1: # definition of a new variable
            # Retrieve the name
            name = extract_name(split_operators[0][0], left=True)
            if name == '_undefined':
                _error('No variable name can be found in ' + equation)
                return []
            # Append the result
            variables.append({'name': name, 'eq': equation.strip(), 'constraint': constraint.strip()})
        elif len(split_operators) == 0: 
            # Continuation of the equation on a new line: append the equation to the previous variable
            variables[-1]['eq'] += ' ' + equation.strip()
            variables[-1]['constraint'] += constraint
        else:
            print 'Error: only one assignement operator is allowed per equation.'
            return []
    return variables 