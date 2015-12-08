import os, sys, socket
from numpy import *
from datetime import datetime, timedelta

def ret_lDTime(iDTime,eDTime,dDTime):
  total_steps = int( (eDTime - iDTime).total_seconds() / dDTime.total_seconds() + 1 )
  return [iDTime + dDTime*i for i in range(total_steps)]

class GSMaP(object):
  def __init__(self, prj="standard",ver="v5"):
    dprjabbr = {\
        "realtime"        :"nrt"\
       ,"standard"        :"mvk"\
       ,"standard_gauge"  :"gauge"\
       ,"reanalysis"      :"rnl"\
       ,"reanalysis_gauge":"rnl"\
       }
    self.dprjabbr = dprjabbr
    self.prjabbr  = dprjabbr[prj]

    if prj == "realtime":
      verfull = ""
    elif (prj == "standard_gauge") & (ver == "v5"):
      verfull = ".v5.222.1.40"
    elif (prj == "standard") & (ver == "v5"):
      verfull = ".v5.222.1"
    elif (prj == "standard_gauge") & (ver == "v6"):
      verfull = ".v6.0000.0"
    elif (prj == "reanalysis") & (ver == "v6"):
      verfull = ".v6.3133.0"

    self.verfull = verfull
    #-- check host --
    hostname = socket.gethostname()
    if hostname == "well":
      if prj == "realtime":
        self.baseDir  = "/media/disk2/data/GSMaP/%s"%(prj)
      else:
        self.baseDir  = "/media/disk2/data/GSMaP/%s.%s"%(prj, ver)

    if hostname in ["mizu","naam"]:
      if prj == "realtime":
        self.baseDir  = "/data2/GSMaP/%s"%(prj)
      else:
        self.baseDir  = "/data2/GSMaP/%s/%s"%(prj,ver)
    #----------------
    
      self.Lat     = arange(-59.95, 59.95+0.01, 0.1)
      self.Lon     = arange(0.05, 359.95+0.01, 0.1)
      self.ny      = len(self.Lat)
      self.nx      = len(self.Lon)
  def load_mmh(self, DTime):
    print DTime
    Year = DTime.year
    Mon  = DTime.month
    Day  = DTime.day
    Hour = DTime.hour
    self.srcDir = os.path.join(self.baseDir, "hourly","%04d"%(Year), "%02d"%(Mon), "%02d"%(Day))
    self.srcPath= os.path.join(self.srcDir, "gsmap_%s.%04d%02d%02d.%02d00%s.dat"%(self.prjabbr, Year,Mon,Day,Hour,self.verfull))
    self.Data   = flipud(fromfile(self.srcPath, float32).reshape(self.ny, self.nx))   # mm/hour
    return self

  def time_ave_mmh(self, iDTime, eDTime, dDTime):
    lDTime = ret_lDTime(iDTime, eDTime, dDTime)
    return (ma.masked_less(array([self.load_mmh(DTime).Data for DTime in lDTime]), 0.0).filled(0.0)).mean(axis=0)

  def time_sum_mmh(self, iDTime, eDTime, dDTime):
    lDTime = ret_lDTime(iDTime, eDTime, dDTime)
    return (ma.masked_less(array([self.load_mmh(DTime).Data for DTime in lDTime]), 0.0).filled(0.0)).sum(axis=0)

  def time_a3dat_mmh(self, iDTime, eDTime, dDTime):
    lDTime = ret_lDTime(iDTime, eDTime, dDTime)
    return ma.masked_less(array([self.load_mmh(DTime).Data for DTime in lDTime]), 0.0).filled(0.0)

  def time_countmiss(self, iDTime, eDTime, dDTime):
    lDTime = ret_lDTime(iDTime, eDTime, dDTime)
    a3dat  = ma.masked_greater(array([self.load_mmh(DTime).Data for DTime in lDTime]), 0.0).filled(0.0)
    a3dat  = ma.masked_less(a3dat, 0.0).filled(1.0)
    return a3dat.sum(axis=0)
