from numpy import *
import datetime
import os
import calendar
#**********************************************
def nearest_idx(aSrc,val):
    ''' return nearest index. by HJKIM'''
    if hasattr(val,'__iter__'): return [abs(aSrc-v).argmin() for v in val]
    else: return abs(aSrc-val).argmin()
#**********************************************
class ibtracs(object):
  def __init__(self):
    self.baseDir = "/media/disk2/data/ibtracs"
    self.Versions= ["v03r04","v03r06"]


  def ret_path(self, Year, ver="v03r06"):
    self.srcDir  = os.path.join(self.baseDir, ver)
    self.srcPath = self.srcDir + "/Year.%04d.ibtracs_all.%s.csv"%(Year,ver)
    return self

  def ret_dlonlat(self,Year, ver="v03r06"):
    srcPath = self.ret_path(Year, ver).srcPath
    lHour   = [0,6,12,18]
    #-- open ----
    f = open(srcPath, "r")
    lines = f.readlines()
    f.close()
    #--- init dict ---
    dout   = {}
    for Mon in range(1,12+1):
      eDay = calendar.monthrange(Year,Mon)[1]
      for Day in range(1,eDay+1):
        for Hour in lHour:
          dout[Year,Mon,Day,Hour] = []
    #-----------------
    for line in lines[3:]:
      line     = line.split(",")
      isotime  = line[6].split(" ")
      date     = map(int, isotime[0].split("-"))
      Year_tmp = date[0]
      Mon      = date[1]
      Day      = date[2]
      Hour     = int(isotime[1].split(":")[0])
      #--- check Year --
      if Year != Year:
        continue
      #--- check Hour --
      if Hour not in lHour:
        continue
      #--- check nature --
      nature   = line[7].strip()
      if nature not in ["TS"]:
        continue
      #-----------------
      tcname   = line[5].strip()
      tcid     = line[0]
      lat      = float(line[16])
      lon      = float(line[17])
      if (lon < 0.0):
        lon = 360.0 + lon
      #-----------------
      dout[Year,Mon,Day,Hour].append((lon,lat))
#      dout[Year,Mon,Day,Hour].append([lon,lat])
    #---
    return dout
  #################################################
  def ret_dpyxy(self, Year, a1lon, a1lat, ver="v03r06"):
    dlonlat = self.ret_dlonlat(Year,ver)
    lkey    = dlonlat.keys()
    dout    = {}
    for key in lkey:
      llonlat = dlonlat[key]
      if len(llonlat)==0:
        dout[key] = []
      else:
        aLon, aLat= zip(*llonlat)
        dout[key] = zip( nearest_idx(a1lon, aLon), nearest_idx(a1lat, aLat) )

    #---
    return dout

 
