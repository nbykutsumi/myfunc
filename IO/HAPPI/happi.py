#! /usr/bin/python
#--------------------------------------------------------------
# CREATED BY : N.Utsumi
#--------------------------------------------------------------
from    numpy           import ma
from    ConfigParser    import SafeConfigParser
from    datetime        import datetime, timedelta 
import   os, sys
import   numpy as np

def read_txtlist(iname):
  f = open(iname, "r")
  lines = f.readlines()
  f.close()
  lines = map(float, lines)
  aout  = np.array(lines, dtype="float32")
  return aout

class Happi():
    def __init__(self):
        self.cfg     = SafeConfigParser(os.environ)
        self.cfg.read("/".join(__file__.split("/")[:-1]) + "/config")
        self.cfg._sections["Defaults"]

        self.baseDir = self.cfg.get("Defaults","baseDir")

    def __call__(self, model, prj, expr, ens):
        """ 
        model  : e.g.) "MIROC5"
        prj    : e.g.) "C20"
        expr   : e.g.) "ALL", "P15", "P20"
        ens    : e.g.) 1, 2, ...
        """
        self.model = model
        self.prj   = prj
        self.expr  = expr
        self.ens   = ens
        self.runName = "%s-%s-%03d"%(prj,expr,ens)
        self.Lat     = read_txtlist( os.path.join(self.baseDir, self.model, "lat.txt"))
        self.Lon     = read_txtlist( os.path.join(self.baseDir, self.model, "lon.txt"))
        self.ny      = 128
        self.nx      = 256
        self.miss    = -999.

    def readslice_float32(self, srcPath, timeslice, ny, nx):
        f = open(srcPath,'rb')

        f.seek(4*timeslice*nx*ny)
        out   = np.fromfile(f,dtype='float32',count=nx*ny)
        f.close()
        return out.reshape(ny,nx)


    def load_6hr(self, var, DTime, maskflag=True, verbose=False):
        if (DTime < datetime(DTime.year, 1, 1, 6)):
            dirYear = DTime.year -1
            dY      = +1
        else:
            dirYear = DTime.year
            dY      = 0

        srcDir  = os.path.join(self.baseDir, self.model, self.runName
                    ,"y%04d"%(dirYear), "6hr")

        srcPath = os.path.join(srcDir
                    ,"%s.sa.1460x%dx%d"%(var, self.ny, self.nx))

        # timeslice for no leap year (e.g.:2001)
        timeslice = (datetime(2001+dY, DTime.month, DTime.day, DTime.hour)
                   - datetime(2001, 1, 1, 6)).total_seconds() / (6*3600)
        if verbose ==True: print srcPath

        out = self.readslice_float32(srcPath, timeslice, self.ny, self.nx)

        if maskflag==True:
            return ma.masked_equal(out, self.miss)
        else:
            return out


    def load_day(self, var, DTime, maskflag=True, verbose=False):
        srcDir  = os.path.join(self.baseDir, self.model, self.runName
                    ,"y%04d"%(DTime.year), "1dy")

        srcPath = os.path.join(srcDir
                    ,"%s.sa.365x%dx%d"%(var, self.ny, self.nx))

        # timeslice for no leap year (e.g.:2001)
        timeslice = (datetime(2001, DTime.month, DTime.day, 0)
                   - datetime(2001, 1, 1, 0)).total_seconds() / (24*3600)

        if verbose ==True: print srcPath

        out = self.readslice_float32(srcPath, timeslice, self.ny, self.nx)

        if maskflag==True:
            return ma.masked_equal(out, self.miss)
        else:
            return out


    def load_mon(self, var, Year, Mon, maskflag=True, verbose=False):
        srcDir  = os.path.join(self.baseDir, self.model, self.runName
                    ,"y%04d"%(Year), "mon")

        srcPath = os.path.join(srcDir
                    ,"%s.sa.12x%dx%d"%(var, self.ny, self.nx))

        if verbose ==True: print srcPath

        out = self.readslice_float32(srcPath, Mon, self.ny, self.nx)

        if maskflag==True:
            return ma.masked_equal(out, self.miss)
        else:
            return out

    def load_const(self, var, miss=False):
        """
        var="topo"
        """
        srcDir  = os.path.join(self.baseDir, self.model, "const")

        srcPath = os.path.join(srcDir
                    ,"%s.%dx%d"%(var, self.ny, self.nx))

        return      np.fromfile(srcPath, dtype="float32").reshape(self.ny, self.nx)
