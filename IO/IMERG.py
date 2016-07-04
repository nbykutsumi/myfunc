from numpy import *
from datetime import datetime, timedelta
import sys

import h5py

def read_hdf5(srcPath, varName, Slice=None, verbose=True):
    """
    COPIED FROM
    # PROGRAM    : read_hdf5.py 
    # CREATED BY : hjkim @IIS.2015-07-13 11:52:15.012270
    """
    h5      = h5py.File(srcPath, 'r')

    if Slice == None:   Slice = slice(None,None,None)

    try:
        h5Var   = h5[varName]
        #aOut    = h5Var[Slice]
        aOut    = h5Var[Slice].T   # By UTSUMI
    except:
        print '!'*80
        print 'I/O Error'
        print 'Blank File? %s'%srcPath
        print 'Blank array will be returned [ %s ]'%varName
        print h5Var.shape
        print Slice
        print '!'*80

        raise ValueError

    if verbose  == True:
        print '\t[READ_HDF5] %s %s -> %s'%( srcPath, h5Var.shape, aOut.shape)

    h5.close()

    return aOut


class IMERG(object):
  def __init__(self, PRD="PROD", VER="V03", crd="sa", BBox=False):
    self.rootDir  = "/tank/utsumi/IMERG/%s/%s"%(PRD, VER)
    self.VER      = VER
    self.crd      = crd
    #----------------
    self.LatOrg  = arange(-89.95, 89.95+0.01, 0.1)

    if   crd=="sa":   # first grid point: South Atlantic
      self.LonOrg  = arange(0.05, 359.95+0.01, 0.1)
    elif crd=="sp":   # first grid point: South Pacific
      self.LonOrg  = arange(-179.95, 179.95+0.01, 0.1)
    else:
      print "check crd",crd
      sys.exit()
 
    self.nyOrg   = len(self.LatOrg)
    self.nxOrg   = len(self.LonOrg)

    if BBox == False:
      self.Lat   = self.LatOrg
      self.Lon   = self.LonOrg
      self.ny    = self.nyOrg
      self.nx    = self.nxOrg
      self.BBox  = BBox
      
    else:
      if   crd=="sa":
        iY = int(round((BBox[0][0]-(-90.0))/0.1))
        iX = int(round((BBox[0][1]-(0.0))/0.1))
        eY = int(round((BBox[1][0]-(-90.0))/0.1))
        eX = int(round((BBox[1][1]-(0.0))/0.1))
      elif crd=="sp":
        iY = int(round((BBox[0][0]-(-90.0))/0.1))
        iX = int(round((BBox[0][1]-(-180))/0.1))
        eY = int(round((BBox[1][0]-(-90.0))/0.1))
        eX = int(round((BBox[1][1]-(-180))/0.1))

      self.iY   = iY
      self.iX   = iX
      self.eY   = eY
      self.eX   = eX
      self.BBox = BBox
      self.Lat   = self.LatOrg[self.iY:self.eY]
      self.Lon   = self.LonOrg[self.iX:self.eX]
      self.ny    = len(self.Lat)
      self.nx    = len(self.Lon)


  def load_mmh(self, DTime, var="precipitationCal"):
    """
    Forward precipitation
    """
    """
    snapshot precipitation - calibrated:      precipitationCal    [mm/hr]
    snapshot precipitation - uncalibrated:    precipitationUncal  [mm/hr]
    calibrated-precipitation random error:    randomError         [mm/hr]
    merged PMW precipitation:                 HQprecipitation     [mm/hr]
    PMW source sensor identifier:             HQprecipSource      [index values]
    PMW source time                           HQobservationTime   [min. into half hour]
    IR precipitation:                         IRprecipitation     [mm/hr]
    Kalman filter weight for IR:              IRkalmanFilterWeight[percent]
    probability of liquid precipitation phase probabilityLiquidPrecipitation [percent]
    """

    Year    = DTime.year
    Mon     = DTime.month
    Day     = DTime.day
    Hour    = DTime.hour
    Minute  = DTime.minute
    srcDir  = self.rootDir + "/%04d/%02d/%02d"%(Year,Mon,Day)
    srcPath = srcDir + "/3B-HHR.MS.MRG.3IMERG.20140402-S120000-E122959.0720.V03D.HDF5"

    #-- Name -----
    eDTime  = DTime + timedelta(minutes=29)
    eHour   = eDTime.hour
    eMinute = eDTime.minute

    Date    = "%04d%02d%02d"%(Year,Mon,Day)
    iTime   = "%02d%02d00"%(Hour,  Minute)
    eTime   = "%02d%02d59"%(eHour,eMinute)
    TotalMinute= "%04d"%( (DTime - datetime(Year,Mon,Day,0,0)).total_seconds()/60.)

    srcPath = srcDir + "/3B-HHR.MS.MRG.3IMERG.20140402-S120000-E122959.0720.V03D.HDF5"
    srcPath = srcDir + "/3B-HHR.MS.MRG.3IMERG.%s-S%s-E%s.%s.%sD.HDF5"\
                      %(Date, iTime, eTime, TotalMinute, self.VER)

    varName = "Grid/%s"%(var)
    #------------- 
    a2dat   = read_hdf5(srcPath, varName, verbose=True)
    if self.crd == "sa":
      a2dat = c_[a2dat[:, self.nxOrg/2:], a2dat[:,:self.nxOrg/2]]

    if self.BBox==False:
      return a2dat
    else:
      return a2dat[self.iY:self.eY, self.iX:self.eX]
 
