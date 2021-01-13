import socket
import os
import pygrib
from numpy import *
from datetime import datetime, timedelta
import numpy as np
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

dbbaseDirDefault = '/home/utsumi/mnt/lab_data2/JRA55'

class anl_p125(object):
    def __init__(self, dbbaseDir=None):
        if dbbaseDir is None:
            self.dbbaseDir = dbbaseDirDefault
        else:
            self.dbbaseDir = dbbaseDir
 
 
    def load_6hr(self, vname, DTime, plev, crd=None):
        '''
        vname= depr, hgt, reld, relv, rh, spfh, strm, tmp, ugrd, vgrd, vpot, vvel
        '''

        Year,Mon,Day,Hour = DTime.timetuple()[:4]
        srcDir = self.dbbaseDir + '/Hist/Daily/anl_p125/%04d%02d'%(Year,Mon)
        srcPath= srcDir + '/anl_p125_%s.%04d%02d%02d%02d'%(vname, Year,Mon,Day,Hour)
    
        with pygrib.open(srcPath) as grbs:
            grb  = grbs.select(level=plev)[0]
            aout = grb.values

        if crd == 'sa':
            aout = np.flipud(aout)

        return aout

class anl_surf125(object):
    def __init__(self, dbbaseDir=None):
        if dbbaseDir is None:
            self.dbbaseDir = dbbaseDirDefault
        else:
            self.dbbaseDir = dbbaseDir

        '''
        variable No.:name:unit
        Use "name" for load
        
        1:Surface pressure:Pa (instant)
        2:Mean sea level pressure:Pa (instant)
        3:2 metre temperature:K (instant)
        4:Potential temperature:K (instant)
        5:Dew point depression (or deficit):K (instant)
        6:2 metre specific humidity:kg kg**-1 (instant)
        8:10 metre U wind component:m s**-1 (instant)
        9:10 metre V wind component:m s**-1 (instant)
        '''

    def load_6hr(self, vname, DTime, crd=None):
        Year,Mon,Day,Hour = DTime.timetuple()[:4]
        srcDir = self.dbbaseDir + '/Hist/Daily/anl_surf125/%04d%02d'%(Year,Mon)
        srcPath= srcDir + '/anl_surf125.%04d%02d%02d%02d'%(Year,Mon,Day,Hour)
    
        with pygrib.open(srcPath) as grbs:
            grb  = grbs.select(name=vname)[0]
            aout = grb.values

        if crd == 'sa':
            aout = np.flipud(aout)

        return aout


class fcst_phy2m125(object):
    def __init__(self, dbbaseDir=None):
        if dbbaseDir is None:
            self.dbbaseDir = dbbaseDirDefault
        else:
            self.dbbaseDir = dbbaseDir

    '''
    variable No.:name:unit
    Use "name" for load
    
    1:Surface pressure:Pa (avg)
    2:Mean evaporation:mm per day (avg)
    3:Mean total precipitation:mm per day (avg)
    4:Mean large scale precipitation:mm per day (avg)
    5:Mean convective precipitation:mm per day (avg)
    6:Mean snowfall rate water equivalent:mm per day (avg)
    7:Latent heat flux:W m**-2 (avg)
    8:Sensible heat flux:W m**-2 (avg)
    9:Momentum flux, u-component:N m**-2 (avg)
    10:Momentum flux, v-component:N m**-2 (avg)
    11:Mean zonal momentum flux by long gravity wave:N m**-2 (avg)
    12:Mean meridional momentum flux by long gravity wave:N m**-2 (avg)
    13:Mean meridional momentum flux by short gravity wave:N m**-2 (avg)
    14:Mean zonal momentum flux by short gravity wave:N m**-2 (avg)
    15:Clear Sky Upward Solar Flux:W m**-2 (avg)
    16:Clear Sky Downward Solar Flux:W m**-2 (avg)
    17:Clear Sky Downward Long Wave Flux:W m**-2 (avg)
    18:Downward short-wave radiation flux:W m**-2 (avg)
    19:Downward long-wave radiation flux:W m**-2 (avg)
    20:Upward short-wave radiation flux:W m**-2 (avg)
    21:Upward long-wave radiation flux:W m**-2 (avg)
    22:Clear Sky Upward Solar Flux:W m**-2 (avg)
    23:Clear Sky Upward Long Wave Flux:W m**-2 (avg)
    24:Downward short-wave radiation flux:W m**-2 (avg)
    25:Upward short-wave radiation flux:W m**-2 (avg)
    26:Upward long-wave radiation flux:W m**-2 (avg)
    '''
 
    def load_3hr(self, vname, DTime, fcst='forward', crd=None):
        if fcst=='forward':  # forward 3-hour average
            pass
        elif fcst=='backward': # backward 3-hour average
            DTime = DTime - timedelta(hours=3)
        else:
            print 'invalid fcst',fcst
            sys.exit()

        Year,Mon,Day,Hour = DTime.timetuple()[:4]
        srcDir = self.dbbaseDir + '/Hist/Daily/fcst_phy2m125/%04d%02d'%(Year,Mon)
        srcPath= srcDir + '/fcst_phy2m125.%04d%02d%02d%02d'%(Year,Mon,Day,Hour)
    
        with pygrib.open(srcPath) as grbs:
            grb  = grbs.select(name=vname)[0]
            aout = grb.values

        if crd == 'sa':
            aout = np.flipud(aout)

        return aout


class fcst_surf125_mon(object):
    def __init__(self, dbbaseDir=None):
        if dbbaseDir is None:
            self.dbbaseDir = dbbaseDirDefault
        else:
            self.dbbaseDir = dbbaseDir
 
 
    def load_mon(self, vname, Year, Mon, crd=None):
        '''
        1:Surface pressure:Pa (avgfc)
        2:Surface roughness:m (avgfc)
        3:Brightness temperature:K (avgfc)::regular_ll:surface:level
        4:Total Cloud Cover:% (avgfc)
        5:High cloud cover:% (avgfc)
        6:Medium cloud cover:% (avgfc)
        7:Low cloud cover:% (avgfc)
        8:Mean sea level pressure:Pa (avgfc)
        9:2 metre temperature:K (avgfc)
        10:Dew point depression (or deficit):K (avgfc)
        11:2 metre specific humidity:kg kg**-1 (avgfc)
        12:2 metre relative humidity:% (avgfc)
        13:10 metre U wind component:m s**-1 (avgfc)
        14:10 metre V wind component:m s**-1 (avgfc)
        '''

        srcDir = self.dbbaseDir + '/Hist/Monthly/fcst_surf125'
        srcPath= srcDir + '/fcst_surf125.%04d%02d'%(Year,Mon)
        with pygrib.open(srcPath) as grbs:
            grb  = grbs.select(vname)[0]
            aout = grb.values

        if crd == 'sa':
            aout = np.flipud(aout)

        return aout



class LL125(object):
    def __init__(self, dbbaseDir=None):
        if dbbaseDir is None:
            self.dbbaseDir = dbbaseDirDefault
        else:
            self.dbbaseDir = dbbaseDir

    def load_const(self, vname, crd=None):
        '''
        Available vnames:
        Geopotential    # surface Geopotential [m^2/s^2]
        Land-sea mask   # surface Land cover (1 = land, 0 = sea)  [Proportion]
        Surface height  # [m], calculate from Geopotential
        '''

        g = 9.80665 # m s-1

        srcDir = self.dbbaseDir + '/Const'
        srcPath= srcDir + '/LL125.grib'

        if vname=='Surface height':
            vnameTmp = 'Geopotential'
        else: vnameTmp = vname

        with pygrib.open(srcPath) as grbs:
            grb  = grbs.select(name=vnameTmp)[0]
            aout = grb.values

        if vname=='Surface height':
            aout = aout / g

        if crd == 'sa':
            aout = np.flipud(aout)

        return aout



def Lat125(crd=None):
    Lat = np.arange(90,-90-0.001, -1.25)
    if crd =='sa':
        Lat = Lat[::-1]
    return Lat

def Lon125(crd=None):
    Lon = np.arange(0,358.75+0.001,1.25)
    return Lon         

def dlatlon125():
    return (1.25, 1.25)

def miss():
    return -9999.

class Jra55_bin(object):
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
    if   var in ["spfh","tmp","ugrd","vgrd","hgt"]:  # "anl_pa125"
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
    else:
        print "check var",var
        print "by JRA55.py"
        print sys.exit()

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





 
