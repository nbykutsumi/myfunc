from numpy import *
from datetime import datetime, timedelta
import GPCP
import GSMaP

#Year    = 2001
#Mon     = 1
iDTime  = datetime(2001,1,1,0)
eDTime  = datetime(2001,1,5,0)
dDTime  = timedelta(hours=1)
prj     = "1dd_v1.2"
gpcp    = GPCP.GPCP(prj)
print gpcp.unit
print gpcp.Lat
print gpcp.TIME
gpcp(iDTime,eDTime)
print shape(gpcp.Data)
a = gpcp.Data
#print shape(a)

gsmap = GSMaP.GSMaP()


b = gsmap.time_ave_mmh(iDTime,iDTime+timedelta(hours=23),timedelta(hours=1))

#d = gsmap.time_countmiss(iDTime,iDTime+timedelta(hours=23),timedelta(hours=1))
