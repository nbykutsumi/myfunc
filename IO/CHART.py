from numpy import *
from datetime import datetime, timedelta
from detect_fsub import *
#import detect_fsub.mk_territory
#from detect_fsub.mk_territory import *
import os

class chart(object):
  def __init__(self):
    self.baseDir    = "/media/disk2/out/chart/ASAS/front"
    self.miss       = -9999.
    self.fronttypes = {"all":0.0,"warm":1.0,"cold":2.0,"occ":3.0,"stat":4.0}
    self.Lon        = arange(0.5, 359.5+0.1, 1.0)
    self.Lat        = arange(-89.5, 89.5+0.1, 1.0)
    self.nx         = 360
    self.ny         = 180

  def load(self, DTime, ftype=False, fill=False):
    srcDir   = os.path.join( self.baseDir, "%04d%02d"%(DTime.year, DTime.month) )
    srcPath  = os.path.join( srcDir, "front.ASAS.%04d.%02d.%02d.%02d.sa.one"%(DTime.year, DTime.month, DTime.day, DTime.hour))
    a2in     = fromfile(srcPath, float32).reshape(self.ny, self.nx)

    if ftype == False:
      return a2in

    else:
      if iterable(ftype)==0:
        if ftype in [0, 0.0]:
          if fill == False:
            return a2in
          else:
            return ma.masked_equal(a2in, self.miss).filled(fill)

        else:
          if fill == False:
            return ma.masked_not_equal(a2in, ftype)
          else:
            return ma.masked_not_equal(a2in, ftype).filled(fill)

      else:
        a2out = array([ma.masked_not_equal(a2in, vtype).filled(0.0) for vtype in ftype]).sum(axis=0)
        if fill == False:
          return ma.masked_equal(a2out, 0.0)
        else:
          return ma.masked_equal(a2out, 0.0).filled(fill)

  

  def territory(self, DTime, ftype=False, rad=False):
    """
      rad : [m], not [km]
    """
    a2in   = self.load(DTime, ftype, self.miss)
    a2terr = detect_fsub.mk_territory(a2in.T, self.Lon, self.Lat, rad, self.miss).T
    return a2terr

  def mk_a2count(self, sDTime, eDTime, dDTime=timedelta(hours=6), ftype=False, rad=False, probability=False):
    """
    if probability ==False: returns  (counts) / (total time steps)
    """
    DTime = sDTime
    a2counts  = zeros([self.ny, self.nx],float32)
    a2one     = ones ([self.ny, self.nx],float32)
    while DTime <= eDTime:
#      print DTime
      a2counts = a2counts + ma.masked_where(self.territory(DTime, ftype, rad)==self.miss, a2one).filled(0.0)
      DTime    = DTime + dDTime


    if probability == True:
      steps    = (eDTime - sDTime).total_seconds() / dDTime.total_seconds() + 1
      a2counts = a2counts / steps
    return a2counts

