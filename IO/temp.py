from numpy import *
from datetime import datetime, timedelta
import RadarAMeDAS
from myfunc.regrid import Regrid
from myfunc.myfunc_fsub import *
from myfunc.regrid.upscale_fsub import *
ra = RadarAMeDAS.RadarAMeDAS(prj="ra_0.01")

DTime = datetime(2014,1,5,0)
a  = ra.loadBackward_mmh(DTime)
print a
LatOrg = ra.Lat
LonOrg = ra.Lon
LatUp  = arange(20.0+0.1/2., 48.+0.1/10., 0.1)
LonUp  = arange(118.0+0.1/2.,150.+0.1/10., 0.1)
us = Regrid.UpScale()
us(LatOrg, LonOrg, LatUp, LonUp,globflag=False)
b      = us.upscale(a, miss_in=-999., miss_out=-9999.)
print b
#print us.a2arease

#LatOrg = arange(20.0+0.1/2., 48.+0.1/10., 0.1)
#LonOrg = arange(118.0+0.1/2, 150.+0.1/10., 0.1)
#LatUp = arange(20.0+0.5/2., 48.+0.5/10., 0.5)
#LonUp = arange(118.0+0.5/2, 150.+0.5/10., 0.5)

#LatOrg = arange(-90.+0.1/2., 90.-0.1/2.+0.1/10., 0.1)
#LonOrg = arange(0.0+0.1/2, 360.-0.1/2. +0.1/10., 0.1)
#LatUp  = arange(-90.+0.5/2., 90.-0.5/2.+0.5/10., 0.5)
#LonUp  = arange(0.0+0.5/2, 360.-0.5/2. +0.5/10., 0.5)

#LatOrg = arange(0.+0.1/2., 90.-0.1/2.+0.1/10., 0.1)
#LonOrg = arange(50.+0.1/2, 360.-0.1/2. +0.1/10., 0.1)
#LatUp  = arange(0.+0.5/2., 90.-0.5/2.+0.5/10., 0.5)
#LonUp  = arange(50.+0.5/2, 360.-0.5/2. +0.5/10., 0.5)


#
#globflag = 1
##globflag = 0
#miss = -9999.  # no need to change
##lupscale_prep  = myfunc_fsub.upscale_prep( \
##                 LonOrg.astype(float32), LatOrg.astype(float32)\
##               , LonUp.astype(float32),  LatUp.astype(float32)\
##               , miss)
#
#lupscale_prep  = upscale_fsub.upscale_prep( \
#                 LonOrg.astype(float32), LatOrg.astype(float32)\
#               , LonUp.astype(float32),  LatUp.astype(float32)\
#               , globflag)
#
#
#a1xw_corres_fort  = lupscale_prep[0]
#a1xe_corres_fort  = lupscale_prep[1]
#a1ys_corres_fort  = lupscale_prep[2]
#a1yn_corres_fort  = lupscale_prep[3]
#a2areasw          = lupscale_prep[4].T
#a2arease          = lupscale_prep[5].T
#a2areanw          = lupscale_prep[6].T
#a2areane          = lupscale_prep[7].T
#nyOrg             = len(LatOrg)
#nxOrg             = len(LonOrg)
#nyUp              = len(LatUp )
#nxUp              = len(LonUp )
#
#print a2arease
#print a2areasw
#print a2areane
#print a2areanw
