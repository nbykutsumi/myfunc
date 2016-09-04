import os, sys, socket
from numpy import *
from datetime import datetime, timedelta
from glob import glob

def ret_lDTime(iDTime,eDTime,dDTime):
  total_steps = int( (eDTime - iDTime).total_seconds() / dDTime.total_seconds() + 1 )
  return [iDTime + dDTime*i for i in range(total_steps)]

class GSMaP(object):
  def __init__(self, prj="standard",ver="v6", BBox=False):
    dprjabbr = {\
        "realtime"        :"nrt"\
       ,"standard"        :"mvk"\
       ,"standard_gauge"  :"gauge"\
       ,"reanalysis"      :"rnl"\
       ,"reanalysis_gauge":"rnl"\
       }
    self.dprjabbr = dprjabbr
    self.prjabbr  = dprjabbr[prj]
    self.ver      = ver
    #-- check host --
    hostname = socket.gethostname()
    if hostname == "well":
      if prj == "realtime":
        self.baseDir  = "/media/disk2/data/GSMaP/%s"%(prj)
      else:
        self.baseDir  = "/media/disk2/data/GSMaP/%s.%s"%(prj, ver)

    if hostname in ["mizu","naam"]:
      if prj == "realtime":
        self.baseDir          = "/data2/GSMaP/%s"%(prj)
        self.baseDirSateinfo  = "/data2/GSMaP/%s.sateinfo"%(prj)
      else:
        self.baseDir          = "/data2/GSMaP/%s/%s"%(prj,ver)
        self.baseDirSateinfo  = "/data2/GSMaP/%s.sateinfo/%s"%(prj,ver)
    #----------------
    self.LatOrg  = arange(-59.95, 59.95+0.01, 0.1)
    self.LonOrg  = arange(0.05, 359.95+0.01, 0.1)
    self.nyOrg   = len(self.LatOrg)
    self.nxOrg   = len(self.LonOrg)
    if BBox == False:
      self.Lat   = self.LatOrg
      self.Lon   = self.LonOrg
      self.ny    = self.nyOrg
      self.nx    = self.nxOrg
      self.BBox  = BBox
    else:
      iY = int(round((BBox[0][0]-(-60.0))/0.1))
      iX = int(round((BBox[0][1]-(0.0))/0.1))
      eY = int(round((BBox[1][0]-(-60.0))/0.1))
      eX = int(round((BBox[1][1]-(0.0))/0.1))
      self.iY   = iY
      self.iX   = iX
      self.eY   = eY
      self.eX   = eX
      self.BBox = BBox
      self.Lat   = self.LatOrg[self.iY:self.eY]
      self.Lon   = self.LonOrg[self.iX:self.eX]
      self.ny    = len(self.Lat)
      self.nx    = len(self.Lon)

  def ret_path_sateinfo(self, DTime):
    Year = DTime.year
    Mon  = DTime.month
    Day  = DTime.day
    Hour = DTime.hour
    ver  = self.ver

    srcDir = os.path.join(self.baseDirSateinfo, "hourly","%04d"%(Year), "%02d"%(Mon), "%02d"%(Day))
    findPath=os.path.join(srcDir, "gsmap_%s.%04d%02d%02d.%02d00.%s.*.sateinfo.dat"%(self.prjabbr, Year,Mon,Day,Hour,self.ver))
    return glob(findPath)[0]

  def load_sateinfo(self, DTime):
    """
    positive: Microwave radiometer
    0       : No satellite observation by both MW and IR
    negative: Only IR observation (No microwave radiometer)
    """
    srcPath = self.ret_path_sateinfo(DTime)
    Data   = flipud(fromfile(srcPath, int32).reshape(self.nyOrg, self.nxOrg))   # mm/hour

    if self.BBox==False:
      return Data
    else:
      return Data[self.iY:self.eY, self.iX:self.eX]

  def ret_path(self, DTime):
    Year = DTime.year
    Mon  = DTime.month
    Day  = DTime.day
    Hour = DTime.hour
    ver  = self.ver
    srcDir = os.path.join(self.baseDir, "hourly","%04d"%(Year), "%02d"%(Mon), "%02d"%(Day))
    findPath=os.path.join(srcDir, "gsmap_%s.%04d%02d%02d.%02d00.%s.*.dat"%(self.prjabbr, Year,Mon,Day,Hour,self.ver))
    return glob(findPath)[0]

  def load_mmh(self, DTime):
    """
    forward mean precipitation rate
    """
    srcPath= self.ret_path(DTime)
    Data   = flipud(fromfile(srcPath, float32).reshape(self.nyOrg, self.nxOrg))   # mm/hour

    if self.BBox==False:
      return Data
    else:
      return Data[self.iY:self.eY, self.iX:self.eX]

  def time_sum_mmh(self, iDTime, eDTime, dDTime):
    lDTime = ret_lDTime(iDTime, eDTime, dDTime)
    #return (ma.masked_less(array([self.load_mmh(DTime).Data for DTime in lDTime]), 0.0).filled(0.0)).sum(axis=0)
    a2dat  = zeros([self.nyOrg,self.nxOrg],float32)
    for DTime in lDTime:
      a2dat = a2dat + ma.masked_less(self.load_mmh(DTime),0.0).filled(0.0)

    if self.BBox==False:
      return a2dat
    else:
      return a2dat[self.iY:self.eY, self.iX:self.eX]


  def time_ave_mmh(self, iDTime, eDTime, dDTime):
    lDTime = ret_lDTime(iDTime, eDTime, dDTime)
    #return (ma.masked_less(array([self.load_mmh(DTime).Data for DTime in lDTime]), 0.0).filled(0.0)).mean(axis=0)
    a2dat  = zeros([self.nyOrg,self.nxOrg],float32)
    for DTime in lDTime:
      a2dat = a2dat + ma.masked_less(self.load_mmh(DTime),0.0).filled(0.0)

    if self.BBox==False:
      return a2dat  /len(lDTime)
    else:
      return a2dat[self.iY:self.eY, self.iX:self.eX] /len(lDTime)

  def time_a3dat_mmh(self, iDTime, eDTime, dDTime):
    lDTime = ret_lDTime(iDTime, eDTime, dDTime)
    if self.BBox==False:
      return ma.masked_less(array([self.load_mmh(DTime) for DTime in lDTime]), 0.0).filled(0.0)
    else:
      return ma.masked_less(array([self.load_mmh(DTime)[self.iY:self.eY, self.iX:self.eX]
             for DTime in lDTime]), 0.0).filled(0.0)




    
  def time_countmiss(self, iDTime, eDTime, dDTime):
    lDTime = ret_lDTime(iDTime, eDTime, dDTime)
    #a3dat  = ma.masked_greater(array([self.load_mmh(DTime).Data for DTime in lDTime]), 0.0).filled(0.0)
    #a3dat  = ma.masked_less(a3dat, 0.0).filled(1.0)
    a2dat  = zeros([self.nyOrg,self.nxOrg],float32)
    for DTime in lDTime:
      a2dat = a2dat + (ma.masked_less(self.load_mmh(DTime), 0.0)*0.0).filled(1.0)

    if self.BBox==False:
      return a2dat
    else:
      return a2dat[self.iY:self.eY, self.iX:self.eX]

