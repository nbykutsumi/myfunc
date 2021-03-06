from numpy import *
from netCDF4 import *
import socket
import os, sys
from datetime import datetime, timedelta
import glob

class M2T1NXSLV(object):
    def __init__(self):
        hostname = socket.gethostname()
        if hostname =='mizu':
            baseDir = '/home/utsumi/mnt/wellshare/data/MERRA2/M2T1NXSLV'
        elif hostname=='well':
            baseDir = '/media/disk2/share/data/MERRA2/M2T1NXSLV'
        else:
            print 'in MERRA2.py'
            print 'check host',hostname
            sys.exit()

        self.baseDir = baseDir
        tmpPath = baseDir + '/u850/199904/u850.MERRA2_200.tavg1_2d_slv_Nx.19990401.nc4'
        nc = Dataset(tmpPath, "r", format="NETCDF")
        self.baseDir = baseDir
        self.Lat = nc.variables["lat"][:]
        self.Lon = nc.variables["lon"][:]
        self.dLat= 0.5
        self.dLon= 0.625
        #self.Lat = arange(-90,90+0.001,self.dLat)
        #self.Lon = arange(-180,179.375,self.dLon)
        self.dvarName = {'u850':'U850', 'v850':'V850', 'u10m':'U10M','v10m':'V10M'}

    def load_var(self, varName, DTime):
        Year,Mon,Day,Hour,Mnt = DTime.timetuple()[:5]
        srcDir = self.baseDir + '/%s/%04d%02d'%(varName, Year, Mon)
        
        ssearch= srcDir + '/%s.MERRA2_???.tavg1_2d_slv_Nx.%04d%02d%02d.nc4'%(varName, Year,Mon,Day)
        srcPath= glob.glob(ssearch)[0]
        try:
            nc = Dataset(srcPath, 'r', format='NETCDF')
        except IOError:
            print 'IOError'
            print 'in MERRA2.py'
            print srcPath
            sys.exit()

        i = Hour
        varNameNC = self.dvarName[varName]
        return nc.variables[varNameNC][i] 



class M2I1NXASM(object):
    def __init__(self):
        hostname = socket.gethostname()
        if hostname =='mizu':
            baseDir = '/home/utsumi/mnt/wellshare/data/MERRA2/M2I1NXASM'
        elif hostname=='well':
            baseDir = '/media/disk2/share/data/MERRA2/M2I1NXASM'
        else:
            print 'in MERRA2.py'
            print 'check host',hostname
            sys.exit()

        self.baseDir = baseDir
        tmpPath = baseDir + '/ps/201404/ps.MERRA2_400.inst1_2d_asm_Nx.20140401.nc4'
        nc = Dataset(tmpPath, "r", format="NETCDF")
        self.baseDir = baseDir
        self.Lat = nc.variables["lat"][:]
        self.Lon = nc.variables["lon"][:]
        self.dLat= 0.5
        self.dLon= 0.625
        #self.Lat = arange(-90,90+0.001,self.dLat)
        #self.Lon = arange(-180,179.375,self.dLon)
        self.dvarName = {'t10m':'T10M', 'qv10m':'QV10M', 'ps':'PS'}


    def load_var(self, varName, DTime):
        Year,Mon,Day,Hour,Mnt = DTime.timetuple()[:5]
        srcDir = self.baseDir + '/%s/%04d%02d'%(varName, Year, Mon)
        
        ssearch= srcDir + '/%s.MERRA2_???.inst1_2d_asm_Nx.%04d%02d%02d.nc4'%(varName, Year,Mon,Day)
        #print ssearch
        try:
            srcPath= glob.glob(ssearch)[0]
        except IndexError:
            print 'IndexError'
            print 'in MERRA2.py'
            print ssearch
            sys.exit()

        try:
            nc = Dataset(srcPath, 'r', format='NETCDF')
        except IOError:
            print 'IOError'
            print 'in MERRA2.py'
            print srcPath
            sys.exit()

        i = Hour
        varNameNC = self.dvarName[varName]
        return nc.variables[varNameNC][i] 


if __name__ == '__main__':
    merra= M2I1NXASM()
    DTime = datetime(2014,4,1,2)
    print merra.Lat.dtype
    print merra.Lon.dtype
    print merra.load_var('PS',DTime)


