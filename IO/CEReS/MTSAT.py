from numpy import *
from datetime import datetime, timedelta
from bisect import bisect, bisect_right
import os, sys, socket


class MTSAT(object):
    def __init__(self):
        #-- check host -
        hostname = socket.gethostname()
        if hostname == "mizu":
            #self.baseDir = "/home/utsumi/mnt/wellshare/data/CEReS"
            self.baseDir = "/data4/utsumi/data/CEReS"
        elif hostname == "well":
            self.baseDir = "/media/disk2/share/data/CEReS"
        else:
            print "In CEReS/MTSAT.py"
            print "Check host",hostname
            sys.exit()

    def __call__(self, sateName="MTSAT-1R", BBox=None):
        self.Lat = arange(-59.98,59.98+0.00001,  0.04) # fliped order!
        self.Lon = arange(80.02, 199.98+0.00001, 0.04)
        self.LatBnd = arange(-60,60+0.00001, 0.04)
        self.LonBnd = arange(80.0, 200.0+0.00001, 0.04)
        self.dlat   = 0.04
        self.dlon   = 0.04
        self.sateName = sateName
        self.ny  = len(self.Lat)
        self.nx  = len(self.Lon)
        self.BBox = BBox
        if BBox !=None:
            [[lat0,lon0],[lat1,lon1]]= BBox
            x0 = bisect_right(self.LonBnd, lon0) -1
            x1 = bisect_right(self.LonBnd, lon1) -1
            y0 = bisect_right(self.LatBnd, lat0) -1
            y1 = bisect_right(self.LatBnd, lat1) -1
            self.Lon = self.Lon[x0:x1+1]
            self.Lat = self.Lat[y0:y1+1]
            self.LonBnd = self.LonBnd[x0:x1+2]
            self.LatBnd = self.LatBnd[y0:y1+2]
            self.x0 = x0
            self.x1 = x1
            self.y0 = y0
            self.y1 = y1

    def load_data(self, DTime, chName=None):
        Year = DTime.year
        Mon  = DTime.month
        Day  = DTime.day
        Hour = DTime.hour
        Mnt  = DTime.minute
        ny, nx = self.ny, self.nx
        srcDir = self.baseDir + "/%s/%04d/%02d%02d"%(self.sateName,Year,Mon,Day)
        srcPath= srcDir + "/%04d%02d%02d%02d%02d_%sbt.grd"%(Year,Mon,Day,Hour,Mnt,chName)

        if self.BBox==None:
            return  flipud( fromfile(srcPath, float32).reshape(ny,nx) )
        else:
            y0,y1,x0,x1 = self.y0, self.y1, self.x0, self.x1
            return  flipud( fromfile(srcPath, float32).reshape(ny,nx) )[y0:y1+1, x0:x1+1]

    def ret_path(self, DTime, chName=None):
        Year = DTime.year
        Mon  = DTime.month
        Day  = DTime.day
        Hour = DTime.hour
        Mnt  = DTime.minute
        srcDir = self.baseDir + "/%s/%04d/%02d%02d"%(self.sateName,Year,Mon,Day)
        return srcDir + "/%04d%02d%02d%02d%02d_%sbt.grd"%(Year,Mon,Day,Hour,Mnt,chName)
    def check_file(self, DTime, chName=None):
        srcPath = self.ret_path(DTime, chName)
        return os.path.exists(srcPath)








