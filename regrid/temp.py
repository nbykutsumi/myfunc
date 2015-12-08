from numpy import *
from datetime import datetime
import JRA55
import Regrid
#from cf import biIntp

model  = "JRA55"
jra    = JRA55.Jra55(res="bn")
LatIn  = jra.Lat
LonIn  = jra.Lon
nyIn   = len(LatIn)
nxIn   = len(LonIn)
a2in   = arange(nyIn*nxIn).reshape(nyIn,nxIn)


Lat    = arange(-89.9,89.9+0.01, 0.2)
Lon    = arange(0.1, 359.9+0.01, 0.2)

#Lat    = arange(-89.75,89.75+0.01, 0.5)
#Lon    = arange(0.25, 359.75+0.01, 0.5)


a2out     = Regrid.biIntp(\
#a2out     = biIntp(\
                 LatIn, LonIn   \
                    , a2in \
                    , Lat, Lon \
                    )
print a2out

