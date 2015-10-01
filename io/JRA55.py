import socket
import os
from numpy import *
from datetime import datetime

#****************************************************
def read_txtlist(iname):
  f = open(iname, "r")
  lines = f.readlines()
  f.close()
  lines = map(float, lines)
  aout  = array(lines, float32)
  return aout

def ret_lDTime(iDTime,eDTime,dDTime):
  total_steps = int( (eDTime - iDTime).total_seconds() / dDTime.total_seconds() + 1 )
  return [iDTime + dDTime*i for i in range(total_steps)]


class Jra55(object):
  def __init__(self, res="bn"):
    #-- check host --
    hostname = socket.gethostname()
    if hostname == "well":  
      self.baseDir  = "/media/disk2/data/JRA55"

    self.Lat = read_txtlist( os.path.join(self.baseDir, "%s.%s"%(res,"anl_p125"), "lat.txt"))
    self.Lon = read_txtlist( os.path.join(self.baseDir, "%s.%s"%(res,"anl_p125"), "lon.txt"))
    self.ny  = len(self.Lat)
    self.nx  = len(self.Lon)
    self.res = res

  def load_6hr(self, var, DTime, lev=False):
    tstep = "6hr"
    Year  = DTime.year
    Mon   = DTime.month
    Day   = DTime.day
    Hour  = DTime.hour
    if   var in ["spfh","tmp","ugrd","vgrd"]:  # "anl_pa125"
      self.srcDir  = os.path.join(self.baseDir, "%s.anl_p125"%(self.res), tstep, var, "%04d"%(Year), "%02d"%(Mon))
      self.srcPath = os.path.join(self.srcDir,  "anl_p125.%s.%04dhPa.%04d%02d%02d%02d.%s"%(var, lev, Year, Mon, Day, Hour, self.res))
      self.prdType = "anl_p125"

    elif var in ["PRMSL"]:
      self.srcDir  = os.path.join(self.baseDir, "%s.anl_surf125"%(self.res), tstep, var, "%04d"%(Year), "%02d"%(Mon))
      self.srcPath = os.path.join(self.srcDir,  "anl_surf125.%s.%04d%02d%02d%02d.%s"%(var, Year, Mon, Day, Hour, self.res))
      self.prdType = "anl_surf125"

    self.Data = fromfile(self.srcPath, float32).reshape(self.ny, self.nx)
    return self


  def load_mon(self, var, Year, Mon, lev=False):
    if var in ["BRTMP"]:
      self.srcDir  = os.path.join(self.baseDir, "%s.fcst_surf125"%(self.res), "Monthly", var, "%04d"%(Year))
      self.srcPath = os.path.join(self.srcDir,  "fcst_surf125.%s.%04d%02d.%s"%(var, Year, Mon, self.res))

    self.Data = fromfile(self.srcPath, float32).reshape(self.ny, self.nx)
    return self


  def time_ave(self, var, iDTime, eDTime, dDTime, lev=False, miss=False):
    lDTime = ret_lDTime(iDTime, eDTime, dDTime)
    print lDTime
    if type(miss)==bool:
      return array([self.load_6hr(var,DTime,lev).Data for DTime in lDTime]).mean(axis=0)
    else:
      print "check this function!! in JRA55.py"
      sys.exit()
#      return ma.masked_equal(array([load_bn(var,DTime,lev).Data for DTime in lDTime]).mean(axis=0), miss).mean(axis=0)
    

  def load_const(self, var, miss=False):
    """
    var="topo", "land"
    """
    if var in ["topo","land"]:
      self.srcDir = "%s/%s.LL125/const"%(self.baseDir, self.res)
      self.srcPath= os.path.join(self.srcDir, "%s.%s"%(var, self.res))

    self.Data   = fromfile(self.srcPath, float32).reshape(self.ny, self.nx)
    return self 