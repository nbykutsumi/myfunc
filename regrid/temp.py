from numpy import *
from datetime import datetime, timedelta
from myfunc.regrid import Regrid2
from myfunc.regrid import Regrid
import myfunc.IO.CLOUDTYPE as CLOUDTYPE
import myfunc.util as util
import calendar
import sys

from mpl_toolkits.basemap import Basemap
 

iYM    = [2014,5]
eYM    = [2014,5]
lYM    = util.ret_lYM(iYM, eYM)
#dattype= "RA"
dattype= "GSMaP"
#dattype= "GSMaP.MW"
#dattype= "GSMaP.IR"
#dattype= "IMERG"
#dattype= "KuPR"
#dattype= "GMI"

BBox    = [[-0.1, 113.875],[52.1, 180.125]]
ny,nx   = 261, 265
miss    = -9999.

# Cloud Type
cl    = CLOUDTYPE.CloudWNP()
LatUp = cl.Lat
LonUp = cl.Lon

# Init Precip
if   dattype.split(".")[0] =="GSMaP":
  import myfunc.IO.GSMaP as GSMaP
  gsmap = GSMaP.GSMaP(prj="standard", ver="v6", BBox=BBox)
  LatOrg= gsmap.Lat
  LonOrg= gsmap.Lon
  us    = Regrid.UpScale()
  us(LatOrg, LonOrg, LatUp, LonUp, globflag=False)

  us2    = Regrid2.UpScale()
  us2(LatOrg, LonOrg, LatUp, LonUp, globflag=False)

elif dattype == "RA":
  import myfunc.IO.RadarAMeDAS as RadarAMeDAS
  ra    = RadarAMeDAS.RadarAMeDAS(prj="ra_0.01")
  #LatOrg= ra.Lat.astype(float32)
  #LonOrg= ra.Lon.astype(float32)

  LatOrg= ra.Lat
  LonOrg= ra.Lon

  LatUpRA = LatUp
  LonUpRA = LonUp
  us    = Regrid.UpScale()
  us(LatOrg, LonOrg, LatUpRA, LonUpRA, globflag=False)

  us2    = Regrid2.UpScale()
  us2(LatOrg, LonOrg, LatUpRA, LonUpRA, globflag=False)



DTime = datetime(2014,5,5,0)
if   dattype =="GSMaP":
  a2prOrg = ma.masked_less(gsmap.load_mmh(DTime),0.0).filled(miss)    # mm/h, forward
  a2pr    = us.upscale(a2prOrg, pergrid=False, miss_in=miss, miss_out=miss)
  a2pr2    = us2.upscale(a2prOrg, pergrid=False, miss_in=miss, miss_out=miss)

elif dattype =="RA":
  a2prOrg = ra.loadForward_mmh(DTime,mask=True).filled(miss)    # mm/h, forward
  a2pr    = us.upscale(a2prOrg, pergrid=False, miss_in=miss, miss_out=miss)
  a2pr2    = us2.upscale(a2prOrg, pergrid=False, miss_in=miss, miss_out=miss)

a2pr = ma.masked_equal(a2pr, -9999.)
a2pr2 = ma.masked_equal(a2pr2, -9999.)

a2d = a2pr2 - a2pr
print a2pr
print a2pr2

