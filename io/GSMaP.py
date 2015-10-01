import os, sys
from numpy import *
from datetime import datetime, timedelta

def ret_lDTime(iDTime,eDTime,dDTime):
  total_steps = int( (eDTime - iDTime).total_seconds() / dDTime.total_seconds() + 1 )
  return [iDTime + dDTime*i for i in range(total_steps)]


class gsmap(object):
  def __init__(self, prj="nrt",ver=False):
    if prj=="nrt":
      self.baseDir = "/media/disk2/data/GSMaP/realtime/archive"
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
    self.srcDir = os.path.join(self.baseDir, "%04d"%(Year), "%02d"%(Mon), "%02d"%(Day))
    self.srcPath= os.path.join(self.srcDir, "gsmap_nrt.%04d%02d%02d.%02d00.dat"%(Year,Mon,Day,Hour))
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
