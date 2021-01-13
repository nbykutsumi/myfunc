# %%
from numpy import *
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import JRA55
import pygrib
#%matplotlib inline


p125 = JRA55.anl_p125()

DTime = datetime(2001,1,1,18)
#vname = 'relv'
#vname = 'tmp'
vname = 'rh'
plev  = 1000
a = p125.load_6hr(vname=vname, DTime=DTime, plev=plev)
print a


baseDir = '/home/utsumi/mnt/lab_data2/JRA55/Hist/Daily/anl_p125'
Year,Mon,Day,Hour = DTime.timetuple()[:4]
srcDir = baseDir + '/%04d%02d'%(Year,Mon)
srcPath= srcDir + '/anl_p125_%s.%04d%02d%02d%02d'%(vname, Year,Mon,Day,Hour)

with pygrib.open(srcPath) as grbs:
    grb  = grbs.select(level=plev)[0]
    aout = grb.values
    lats,lons= grb.latlons()
print lats
print ''
print lons
#grbs.seek()

#plt.imshow(a,origin='lower')
plt.imshow(a)
plt.show()

# %%
