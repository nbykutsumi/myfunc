from   numpy import *
from   netCDF4 import *
import os, sys, socket
class MERGIR(object):
    def __init__(self):

        #-- check host ---
        hostname = socket.gethostname()
        if hostname == "mizu":
            baseDir = "/home/utsumi/mnt/wellshare/data/MERGIR"
        elif hostname == "well":
            baseDir = "/media/disk2/share/data/MERGIR"
        else:
            print "In MERGIR.py"
            print "Check host",hostname
            sys.exit()

        self.baseDir = baseDir
        tmpPath      = baseDir + "/2014/0401/merg_2014040100_4km-pixel.nc4"
        nc = Dataset(tmpPath, "r", format="NETCDF")
        self.Lat = nc.variables["lat"][:]
        self.Lon = nc.variables["lon"][:]

    def load_1hr(self,DTime):
        Year    = DTime.year
        Mon     = DTime.month
        Day     = DTime.day
        Hour    = DTime.hour
        srcPath = self.baseDir + "/%04d/%02d%02d/merg_%04d%02d%02d%02d_4km-pixel.nc4"%(Year,Mon,Day,Year,Mon,Day,Hour)

        print srcPath
        nc  = Dataset(srcPath,"r", format="NETCDF")
        return nc.variables["Tb"][:]

    def load_30min(self,DTime):
        Year    = DTime.year
        Mon     = DTime.month
        Day     = DTime.day
        Hour    = DTime.hour
        Mnt     = DTime.minute
        idx     = {0:0, 30:1}
        srcPath = self.baseDir + "/%04d/%02d%02d/merg_%04d%02d%02d%02d_4km-pixel.nc4"%(Year,Mon,Day,Year,Mon,Day,Hour)

        print srcPath
        nc  = Dataset(srcPath,"r", format="NETCDF")
        return nc.variables["Tb"][idx[Mnt]]






