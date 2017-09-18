import sys, os, importlib
import socket
from numpy        import *
from pyhdf        import SD
from ConfigParser import SafeConfigParser


class L3A25(object):
    def __init__(self, version="07",GRIDTYPE=2, crd='sa', BBox=False):
        '''
        GRIDTYPE=1: 5   degree
        GRIDTYPE=2: 0.5 degree

        Note:
        The origin of the original data is SouthWest. This can be found on HDF4 file header as:
        "Origin=SOUTHWEST"

        '''

        self.sensor  = "TRMM.PR"
        self.prdName = "L3A25"
        self.version = version
        self.crd     = crd

        self.hostname= socket.gethostname()
        if   self.hostname=="well":
            self.rootDir  = "/media/disk2/share/data/GPM"
        elif self.hostname=="mizu":
            self.rootDir  = "/home/utsumi/mnt/wellshare/data/GPM"

        # Config
        self.cfg        = SafeConfigParser( os.environ )
        self.cfg.read("/".join(__file__.split("/")[:-1]) + "/config")
        #self.cfg._sections["Defaults"].update( kwargs )

        # read_hdf function
        fnPath          = self.cfg.get("Defaults","hdf4_module")
        fnName          = fnPath.split(".")[-1]
        modPath         = ".".join( fnPath.split(".")[:-1] ) 
        self.func_read  = getattr( importlib.import_module( modPath ), fnName) 

        # Lat & Lon
        if GRIDTYPE==1:
            self.LatOrg = arange(-40+5*0.5,40-5*0.5+0.01, 5)

            if   crd=="sp":
                self.LonOrg = arange(-180+5*0.5, 180-5*0.5+0.01, 5)   
            elif crd=="sa":
                self.LonOrg = arange(0.0+5*0.5, 360-5*0.5+0.01, 5)
            else:
                print "check crd",crd
                sys.exit()

            self.dLat   = 5.0
            self.dLon   = 5.0


        elif GRIDTYPE==2:
            self.LatOrg = arange(-37+0.5*0.5, 37-0.5*0.5+0.01, 0.5)

            if   crd =="sp":
                self.LonOrg = arange(-180+0.5*0.5, 180-0.5*0.5+0.01, 0.5)
            elif crd =="sa":
                self.LonOrg = arange(0.0+0.5*0.5, 360-0.5*0.5+0.01, 0.5)
            else:
                print "check crd",crd
                sys.exit()

            self.dLat   = 0.5
            self.dLon   = 0.5

        else:
            print 'check GRIDTYPE'
            sys.exit()


        self.nxOrg = len(self.LonOrg)
        self.nyOrg = len(self.LatOrg)

        # BBox
        if BBox == False:
            self.Lat= self.LatOrg
            self.Lon= self.LonOrg


        else:
            self.iY = int(round((BBox[0][0]-self.LatOrg[0])/self.dLat))
            self.iX = int(round((BBox[0][1]-self.LonOrg[0])/self.dLon))
            self.eY = int(round((BBox[1][0]-self.LatOrg[0])/self.dLat))
            self.eX = int(round((BBox[1][1]-self.LonOrg[0])/self.dLon))
            self.Lat= self.LatOrg[self.iY:self.eY]
            self.Lon= self.LonOrg[self.iX:self.eX]

        self.ny = len(self.Lat)
        self.nx = len(self.Lon)
        self.BBox = BBox


    def load_var(self,Year,Mon,Var="rainMean2"):
        srcDir = os.path.join(self.rootDir, self.sensor, self.prdName, self.version, "%04d"%(Year), "%02d"%(Mon))


        lfileName = os.listdir(srcDir)
        if len(lfileName) != 1:
            print "multiple files in ", srcDir
            print lfileName
            sys.exit()
        fileName = lfileName[0]
        srcPath = os.path.join(srcDir,fileName)

        print srcPath


        aTmp = self.func_read(srcPath, Var, Slice=None, verbose=True)

        #--------------

        if len(aTmp.shape)==3:
            nz,nx,ny   = aTmp.shape
        elif len(aTmp.shape)==2:
            nz         = 1
            nx,ny      = aTmp.shape
            aTmp       = aTmp.reshape(1,nx,ny)
 
        aOut = empty([nz,ny,nx])

        for i in range(nz):
            aOut[i] = (aTmp[i].T)
            if self.crd == 'sa':
                 aOut[i] = c_[aOut[i,:, self.nxOrg/2:], aOut[i, :, :self.nxOrg/2]]



        if self.BBox == False:
            return aOut
        else:
            return aOut[:,self.iY:self.eY, self.iX:self.eX]
 

        return aOut

