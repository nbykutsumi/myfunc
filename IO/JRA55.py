import socket
import os
from numpy import *
from datetime import datetime
#-- test @ 27th Oct ---
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
  def __init__(self, res="145x288"):
    #-- check host --
    hostname = socket.gethostname()
    if hostname == "well":  
      self.baseDir  = "/media/disk2/data/JRA55"
    if hostname in ["mizu","naam"]:  
      self.baseDir  = "/tank/utsumi/data/JRA55"
    #----------------
    self.Lat = read_txtlist( os.path.join(self.baseDir, "%s.%s"%(res,"anl_p125"), "lat.txt"))
    self.Lon = read_txtlist( os.path.join(self.baseDir, "%s.%s"%(res,"anl_p125"), "lon.txt"))
    self.ny  = len(self.Lat)
    self.nx  = len(self.Lon)
    self.res = res
    self.miss= -9999.

  def path_6hr(self, var, DTime, lev=False):
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
    elif var in ["PWAT"]:
      self.srcDir  = os.path.join(self.baseDir, "%s.anl_column125"%(self.res), tstep, var, "%04d"%(Year), "%02d"%(Mon))
      self.srcPath = os.path.join(self.srcDir,  "anl_column125.%s.%04d%02d%02d%02d.%s"%(var, Year, Mon, Day, Hour, self.res))
      self.prdType = "anl_column125"
    elif var in ["APCP"]:
      """
      APCP: mm/day
      """
      self.srcDir  = os.path.join(self.baseDir, "%s.fcst_phy2m125"%(self.res), tstep, var, "%04d"%(Year), "%02d"%(Mon))
      self.srcPath = os.path.join(self.srcDir,  "fcst_phy2m125.%s.%04d%02d%02d%02d.%s"%(var, Year, Mon, Day, Hour, self.res))
      self.prdType = "fcst_surf125"

    return self


  def load_6hr(self, var, DTime, lev=False):
    srcPath   = self.path_6hr(var, DTime, lev).srcPath
    return fromfile(srcPath, float32).reshape(self.ny, self.nx)


  def path_3hr(self, var, DTime, lev=False):
    tstep = "3hr"
    Year  = DTime.year
    Mon   = DTime.month
    Day   = DTime.day
    Hour  = DTime.hour
    if var in ["APCP"]:
      self.srcDir  = os.path.join(self.baseDir, "%s.fcst_phy2m125"%(self.res), tstep, var, "%04d"%(Year), "%02d"%(Mon))
      self.srcPath = os.path.join(self.srcDir,  "fcst_phy2m125.%s.%04d%02d%02d%02d.%s"%(var, Year, Mon, Day, Hour, self.res))
      self.prdType = "fcst_surf125"

    return self

  def load_3hr(self, var, DTime, lev=False):
    srcPath   = self.path_3hr(var, DTime, lev).srcPath
    return fromfile(srcPath, float32).reshape(self.ny, self.nx)

  def path_mon(self, var, Year, Mon, lev=False):
    if var in ["BRTMP"]:
      self.srcDir  = os.path.join(self.baseDir, "%s.fcst_surf125"%(self.res), "Monthly", var, "%04d"%(Year))
      self.srcPath = os.path.join(self.srcDir,  "fcst_surf125.%s.%04d%02d.%s"%(var, Year, Mon, self.res))
    elif var in ["PWAT"]:
      self.srcDir  = os.path.join(self.baseDir, "%s.anl_column125"%(self.res), "Monthly", var, "%04d"%(Year))
      self.srcPath = os.path.join(self.srcDir,  "anl_column125.%s.%04d%02d.%s"%(var, Year, Mon, self.res))
    elif var in ["APCP"]:
      self.srcDir  = os.path.join(self.baseDir, "%s.fcst_phy2m125"%(self.res), "Monthly", var, "%04d"%(Year))
      self.srcPath = os.path.join(self.srcDir,  "fcst_phy2m125.%s.%04d%02d.%s"%(var, Year, Mon, self.res))

    return self

  def load_mon(self, var, Year, Mon, lev=False):
    srcPath   = self.path_mon(var, Year, Mon, lev).srcPath
    return    fromfile(srcPath, float32).reshape(self.ny, self.nx)

  def load_mon_prcp_mmd(self, Year, Mon):
    return self.load_mon("APCP", Year, Mon)  # mm/day

  def load_mon_prcp_mmh(self, Year, Mon):
    return self.load_mon("APCP", Year, Mon) /(24.) 

  def load_mon_prcp_mms(self, Year, Mon):
    return self.load_mon("APCP", Year, Mon) /(60*60*24.) 

  def time_ave(self, var, iDTime, eDTime, dDTime, lev=False, miss=False, verbose=True):
    lDTime = ret_lDTime(iDTime, eDTime, dDTime)
    if verbose==True:
      print lDTime

    if type(miss)==bool:
      return array([self.load_6hr(var,DTime,lev) for DTime in lDTime]).mean(axis=0)
    else:
      print "check this function!! in JRA55.py"
      sys.exit()
#      return ma.masked_equal(array([load_bn(var,DTime,lev).Data for DTime in lDTime]).mean(axis=0), miss).mean(axis=0)
    

  def path_const(self, var):
    if var in ["topo","land"]:
      self.srcDir = "%s/%s.LL125/const"%(self.baseDir, self.res)
      self.srcPath= os.path.join(self.srcDir, "%s.%s"%(var, self.res))
    return self


  def load_const(self, var, miss=False):
    """
    var="topo", "land"
    """
    srcPath     = self.path_const(var).srcPath
    return      fromfile(srcPath, float32).reshape(self.ny, self.nx)

  def path_clim8110(self, var, Mon, lev=False):
    if var in ["PRMSL"]:
      self.srcDir  = os.path.join(self.baseDir, "%s.anl_surf125"%(self.res), "clim8110")
      self.srcPath = os.path.join(self.srcDir,  "anl_surf125.%s.%02d.%s"%(var, Mon, self.res))

    elif var in ["vvel","vpot","vgrd","ugrd","tmp","strm","spfh","rh","relv","reld","hgt","depr"]:
      self.srcDir  = os.path.join(self.baseDir, "%s.anl_p125"%(self.res), "clim8110")
      self.srcPath = os.path.join(self.srcDir,  "anl_p125.%s.%04dhPa.%02d.%s"%(var, Mon, lev, self.res))
    return self

  def load_clim8110(self, var, DTime, lev=False):
    srcPath   = self.path_clim8110(var, DTime, lev).srcPath
    return fromfile(srcPath, float32).reshape(self.ny, self.nx)





 
