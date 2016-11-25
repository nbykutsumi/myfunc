#! /usr/bin/python
#--------------------------------------------------------------
# CREATED BY : N.Utsumi
# BASED ON   : GPyM module by hjkim
#--------------------------------------------------------------
import  os,sys
from    numpy      import array
from    pyhdf      import HDF, VS
from    itertools  import chain

def get_location(srcPath, fn_read):
    Lat    = fn_read( srcPath, 'Latitude' )
    Lon    = fn_read( srcPath, 'Longitude')

    return array( [Lat, Lon] )

#def get_location(srcPath):
#    f = HDF.HDF(srcPath)
#    vs = f.vstart()
#    instLat = vs.attach("Latitude")
#    instLon = vs.attach("Longitude")
#    Lat  = instLat[:]
#    Lon  = instLon[:]
#    
#    instLat.detach()
#    instLon.detach()
#    vs.end()
#    f.close()
#    
#    Lat  = list(chain.from_iterable(Lat))
#    Lon  = list(chain.from_iterable(Lon))
#
#    return array( [Lat, Lon] )
