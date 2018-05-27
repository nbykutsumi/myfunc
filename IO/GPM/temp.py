import myfunc.IO.GPM as GPM
from numpy import *
import myfunc.IO.GSMaP as GSMaP

sensor  = 'TRMM.TMI'
prdName = '2A-CLIM'
prdVer  = 'V05'
minorVer= 'A'


gpm = GPM.L2A_GPROF_HDF5(sensor=sensor, prdName=prdName, version=prdVer, minorversion=minorVer)


