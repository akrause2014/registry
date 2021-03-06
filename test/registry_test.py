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

from dispel4py.registry import registry
registry.initRegistry()

from dispel4py.test.TestFunction1 import add

if __name__ == '__main__':
   print "2 + 7 = %s" % add(2, 7)

   reg = registry.VerceRegistry()

   functionName = "dispel4py.test.TestFunction345"
   reg.register_function(functionName, 'add', 'test/TestFunction.py')

   reg.delete(functionName)

   peName = "dispel4py.test.TestPE999"
   reg.register_pe(peName, 'MyPE', 'test/MyPE.py')

   from dispel4py.test.TestPE999 import MyPE
   pe = MyPE()
   outputs = pe.process({"in1":1, "in2":2})
   print "Result = %s" % outputs[0]["out1"]

   reg.delete(peName)

