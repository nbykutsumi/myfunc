from numpy import *
from datetime import datetime, timedelta
import sys, os, socket

class RadarAMeDAS(object):
  def __init__(self,prj="ra_0.01"):
    hostname = socket.gethostname()
    if hostname == "mizu":
      if prj=="ra_0.01":
        self.baseDir = "/data1/hjkim/AMeDAS/ra_0.01"
      elif prj=="ra_0.1":
        self.baseDir = "/tank/utsumi/data/RadarAMeDAS/ra_0.1"
      else:
        print "invalid prj:",prj 
        sys.exit()
    else:
      print "invalid hostname:", hostname
      sys.exit()

    if prj  =="ra_0.01":
      self.res = 0.01
    elif prj=="ra_0.1":
      self.res = 0.1

    self.unit  = "mm/h"
    self.BBox  = [[20., 118.],[48., 150.]]
    self.Lat   = arange(self.BBox[0][0]+self.res/2,
                        self.BBox[1][0]+self.res/10,
                        self.res, dtype='float64')

    self.Lon   = arange(self.BBox[0][1]+self.res/2,
                        self.BBox[1][1]+self.res/10,
                        self.res, dtype='float64') 
   
    self.ny    = len(self.Lat)
    self.nx    = len(self.Lon) 
    self.miss  = -999.

  def loadBackward_mmh(self,DTime, mask=False):
    """
    original data: "backward" precipitation in mm/hour
    see 
    """
    Year, Mon, Day, Hour, Min =\
      DTime.year, DTime.month, DTime.day, DTime.hour, DTime.minute
    srcDir  = os.path.join(self.baseDir, "%04d%02d"%(Year,Mon))
    srcPath = os.path.join(srcDir, "RadarAmedas.%04d%02d%02d%02d%02d00.%dx%d"%(Year,Mon,Day,Hour,Min,self.ny,self.nx))
    if mask==True:
      return ma.masked_equal(flipud(fromfile(srcPath, float32).reshape(self.ny, self.nx)), self.miss)
    else:
      return flipud(fromfile(srcPath, float32).reshape(self.ny, self.nx))
 
  def loadForward_mmh(self,DTime, mask=False):
    return self.loadBackward_mmh(DTime+timedelta(hours=1), mask=mask) 



