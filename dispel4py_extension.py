# Copyright (c) The University of Edinburgh 2014
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
The IPython extension for viewing and listing modules from the Dispel4Py registry.
'''

from dispel4py.registry import core, client

import sys
import os
import  tempfile
import traceback
import random

from IPython.html.widgets import interact, interactive, fixed
from IPython.html import widgets
from IPython.display import display

def _initRegistry():
    client.config = client.configure()
    return client._initRegistry()
    
def _listPackages(pkg):
    reg = _initRegistry()
    try:
        pkgs = reg.listPackages(pkg)
        return [p for p in pkgs if not p.endswith('__impl') and not p.endswith('__gendef') and not p == pkg]
    except:
        objs = []

def _listObjects(name):
    reg = _initRegistry()
    try:
        objs = reg.list(name)
    except core.UnknownPackageException:
        objs = []
    return objs
    
def _edit(name):
    reg = _initRegistry()
    try:
        source = reg.get_code(name)
        w = widgets.TextareaWidget(
            description=name,
            value=source
        )
        b = widgets.ButtonWidget(description='Update')
        return (reg,w,b)
    except Exception as err:
        import traceback
        traceback.print_exc()
        sys.stderr.write("An error occurred:\n%s\n" % err)
        sys.exit(-1)

def _init_reg_widgets():
    txName = widgets.TextWidget(description='Name: ', value='')
    txName2 = widgets.TextWidget(description='', value='')
    txCode = widgets.TextareaWidget(description='Code: ', value='')
    btSave = widgets.ButtonWidget(description='Save')
    return (txName, txName2, txCode, btSave)

def _make_temp_file(suffix, code):
    r = str(random.randint(0, 999999999999))
    fname = 'tmp_' + r + '_' + suffix
    f = open(fname, 'w')
    f.write(code)
    f.close()
    return fname

from IPython.core.magic import (Magics, magics_class, line_magic)
    
@magics_class
class Dispel4PyMagics(Magics):
    '''
    Creates the dispel4py command in iPython, to be used interactively for training and other purposes.  
    '''

    # XXX : appears to be necessary evil ... need to think of a workaround
    name_to_update = None
    code_to_update = None
    reg_for_update = None
    textarea_for_update = None
    
    txNameSavePE = None
    txClassNameSavePE = None
    txCodeSavePE = None
    btSaveSavePE = None
    regRegPe = None
    
    txNameSaveFn = None
    txFunctionNameSaveFn = None
    txCodeSaveFn = None
    btSaveSaveFn = None
    regRegFn = None
    
    def _update(self, b):
        try: 
            if not self.textarea_for_update is None and not self.textarea_for_update.value is None and not self.name_to_update is None and not self.code_to_update is None and not self.reg_for_update is None:
                self.reg_for_update.update_code(self.name_to_update, self.textarea_for_update.value)
            self.name_to_update = self.code_to_update = self.reg_for_update = None
            print self.textarea_for_update.description, 'updated.'
        except Exception as err:
            import traceback
            traceback.print_exc()
            sys.stderr.write("An error occurred:\n%s\n" % err)
    
    
    def _register_pe(self, b):
        try:
            fname = _make_temp_file(self.txNameSavePE.value, self.txCodeSavePE.value)
            self.regRegPe.register_pe(
                self.txNameSavePE.value,
                self.txClassNameSavePE.value,
                fname
            )
            print 'Registered ' + self.txNameSavePE.value
        except Exception as err:
            import traceback
            traceback.print_exc()
            sys.stderr.write("An error occurred:\n%s\n" % err)
    
    def _register_fn(self, b):
        try:
            fname = _make_temp_file(self.txNameSaveFn.value, self.txCodeSaveFn.value)
            self.regRegFn.register_function(
                self.txNameSaveFn.value,
                self.txFunctionNameSaveFn.value,
                fname
            )
            print 'Registered ' + self.txNameSaveFn.value
        except Exception as err:
            import traceback
            traceback.print_exc()
            sys.stderr.write("An error occurred:\n%s\n" % err)
                
    @line_magic
    def dispel4py(self, line):
        command = line.split()
        if command[0] == 'edit':
            if len(command) == 1:
                print 'Name not provided.'
            reg, w, b = _edit(command[1])
            self.textarea_for_update = w
            display(w)
            display(b)
            self.reg_for_update = reg
            self.name_to_update = w.description
            self.code_to_update = w.value
            b.on_click(self._update)
        elif command[0] == 'register_pe':
            self.regRegPe = _initRegistry()
            self.txNameSavePE, self.txClassNameSavePE, self.txCodeSavePE, self.btSaveSavePE = _init_reg_widgets()
            display(self.txNameSavePE)
            self.txClassNameSavePE.description = 'Class name:'
            display(self.txClassNameSavePE)
            display(self.txCodeSavePE)
            display(self.btSaveSavePE)
            self.btSaveSavePE.on_click(self._register_pe)
        elif command[0] == 'register_fn':
            self.regRegFn = _initRegistry()
            self.txNameSaveFn, self.txFunctionNameSaveFn, self.txCodeSaveFn, self.btSaveSaveFn = _init_reg_widgets()
            display(self.txNameSaveFn)
            self.txFunctionNameSaveFn.description = 'Function name:'
            display(self.txFunctionNameSaveFn)
            display(self.txCodeSaveFn)
            display(self.btSaveSaveFn)
            self.btSaveSaveFn.on_click(self._register_fn)
        elif command[0] == 'list' and len(command) == 1:
            reg = _initRegistry()
            client.list(reg)        
        elif command[0] == 'list':
            pkgs = _listPackages(command[1])
            if pkgs: 
                print "Packages:"
                for p in pkgs: print '  ' + p
            objs = _listObjects(command[1])
            pes = []
            functions = []
            for obj in objs:
                 if obj['type'] == 'eu.verce.registry.domains.PESig':
                     pes.append(obj['name'])
                 if obj['type'] == 'eu.verce.registry.domains.FunctionSig':
                     functions.append(obj['name'])
            if pes: 
                print "Processing Elements:"
                for p in pes: print '  ' + p
            if functions:
                print "Functions:"
                for f in functions: print '  ' + f
        elif command[0] == 'view':
            try:
                reg = _initRegistry()
                source = reg.get_code(command[1])
                if source is None:
                    print "Resource '%s' not found\n" % name
                else:
                    print source
            except Exception as err:
                print traceback.format_exc()
                print "An error occurred."
        elif command[0] == 'workspace':
            try:
                reg = _initRegistry()
                client.workspace(reg)
            except Exception as err:
                print traceback.format_exc()
                print "An error occurred."
        elif command[0] == 'clone':
            try:
                reg = _initRegistry()
                client.clone_workspace(reg)
            except Exception as err:
                print traceback.format_exc()
                print "An error occurred."
        else:
            print "Unknown command '%s'" % line
            
def load_ipython_extension(ip):
    ip.register_magics(Dispel4PyMagics)

def unload_ipython_extension(ipython):
    # If you want your extension to be unloadable, put that logic here.
    None
