from numpy import *
from grids import *
from upscale_fsub import *
from bisect import bisect

def biIntp(Lat,Lon,z,LAT,LON,miss=-999):
    #***********************
    # biIntp
    # by hjkim, modified by N.Utsumi
    #***********************
    #nProc   = MP.cpu_count() if mp==True else 1

    #if type(mp) == int: nProc = mp

    #nProc   = settings.MAX_PROC if nProc > settings.MAX_PROC else nProc


    if Lat[1]>Lat[0] and LAT[1]>LAT[0]:     # in & out : -89.5 ~ 89.5
        sliceInLat  = None
        sliceOutLat = None
        sliceInZ    = None
        sliceOutZ   = None

    elif Lat[0]>Lat[1] and (LAT[0]>LAT[1]): # in & out :  89.5 ~ -89.5
        sliceInLat  = -1
        sliceOutLat = -1
        sliceInZ    = -1
        sliceOutZ   = -1

    elif Lat[0]>Lat[1] and (LAT[1]>LAT[0]): # in 89.5 ~ -89.5, out : -89.5 ~ 89.5
        sliceInLat  = -1
        sliceOutLat = None
        sliceInZ    = -1
        sliceOutZ   = None

    elif Lat[1]>Lat[0] and (LAT[0]>LAT[1]): # in -89.5 ~ 89.5, out : 89.5 ~ -89.5
        sliceInLat  = None
        sliceOutLat = -1
        sliceInZ    = None
        sliceOutZ   = -1

    else:
        raise ValueError,'coord mismatch!!'

    return gridsintp(
                     Lon,Lat[::sliceInLat],
                     z[::sliceInZ].T,
                     LON,LAT[::sliceOutLat],miss
                     ).T[...,::sliceOutZ,:]

class UpScale(object):
  def __init__(self):
    pass
  def __call__(self, LatOrg, LonOrg, LatUp, LonUp, globflag):
    """
    Lat, Lon: 1-d array 
    globflag = False: for regional
    globflag = True : for global data (left of left-most grid is the right-most grid)
    """
    if globflag==True:
      globflag=1
    elif globflag==False:
      globflag=0
    else:
      print "invalid globflag:",globflag
      sys.exit()

    lupscale_prep  = upscale_fsub.upscale_prep( \
                     LonOrg.astype(float32), LatOrg.astype(float32)\
                   , LonUp.astype(float32),  LatUp.astype(float32)\
                   , globflag)

    self.a1xw_corres_fort  = lupscale_prep[0]
    self.a1xe_corres_fort  = lupscale_prep[1]
    self.a1ys_corres_fort  = lupscale_prep[2]
    self.a1yn_corres_fort  = lupscale_prep[3]
    self.a2areasw          = lupscale_prep[4].T
    self.a2arease          = lupscale_prep[5].T
    self.a2areanw          = lupscale_prep[6].T
    self.a2areane          = lupscale_prep[7].T
    self.nyOrg             = len(LatOrg)
    self.nxOrg             = len(LonOrg)
    self.nyUp              = len(LatUp )
    self.nxUp              = len(LonUp )

  def upscale(self, a2org, pergrid=False, miss_in=False, miss_out=False):
    """
    pergrid = False (0): per area (e.g. mm/m2), others (e.g, K, kg/kg, mm/s)
    pergrid = True  (1): per grid (e.g. km2/grid, population/grid)
    missflag= False (0): nocheck for missing value
    missflag= True  (1): check missing value
    """
    if pergrid  == False:
      pergrid  = 0
    else:
      pergrid  = 1
    if type(miss_in) == bool:
      missflag = 0
      miss_in  = -9999. # dummy
      miss_out = -9999. # dummy
    else:
      missflag = 1
      if type(miss_out)==bool:
        print "invalid miss_out:",miss_out
        sys.exit()
    
    return ma.masked_invalid(
            upscale_fsub.upscale_fast(a2org.T\
             , self.a1xw_corres_fort, self.a1xe_corres_fort\
             , self.a1ys_corres_fort, self.a1yn_corres_fort\
             , self.a2areasw.T,       self.a2arease.T\
             , self.a2areanw.T,       self.a2areane.T\
             , self.nxUp,             self.nyUp\
             , pergrid, missflag, miss_in, miss_out\
             ).T
            ).filled(miss_out) 

 
