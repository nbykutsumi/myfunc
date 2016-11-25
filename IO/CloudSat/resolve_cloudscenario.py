#! /usr/bin/python
#--------------------------------------------------------------
# CREATED BY : N.Utsumi
# BASED ON   : GPyM module by hjkim
#--------------------------------------------------------------
import os,sys
from   numpy   import array, shape

def Resolve_CloudScenario(aIn):
  Shape= shape(aIn)
  aIn  = aIn.flatten().astype(int)
  aOut = array([format(v, '016b')[-5:-1] for v in aIn]).reshape(Shape)
  #aOut  = array([format(v,'016b')[-5:-1] for v in aIn.astype(int)])
  return aOut  




