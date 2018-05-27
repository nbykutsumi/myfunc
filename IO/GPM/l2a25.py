import  sys, os, importlib
import  socket
import  glob
from    numpy        import *
from    pyhdf        import SD
from    alien        import read_hdf4
import  functions

class L2A25(object):
    def __init__(self, version="07"):
        self.sensor  = "TRMM.PR"
        self.prdName = "L2A25"
        self.version = version


        self.hostname= socket.gethostname()
        if   self.hostname=="well":
            self.rootDir  = "/media/disk2/share/data/GPM"
        elif self.hostname=="mizu":
            self.rootDir  = "/home/utsumi/mnt/wellshare/data/GPM"
            #self.rootDir  = "/work/a01/utsumi/data/GPM"

        ## read_hdf function
        self.func_read  = read_hdf4.read_hdf4


    def load_var_granule(self,srcPath=None,Var=None,verbose=False):
        aOut    = self.func_read(srcPath, Var, Slice=None, verbose=verbose)
        return  aOut


    def list_granule(self, Year, Mon):
        srcDir  = os.path.join(self.rootDir,\
                               self.sensor ,\
                               self.prdName,\
                               self.version,\
                               "%04d"%(Year),\
                               "%02d"%(Mon),\
                              )
        
        lPath  = glob.glob(srcDir+"/T1PR*")
        return lPath

    def load_dtime_granule(self, srcPath=None):
        return functions.get_dtime_trmm(srcPath, self.load_var_granule)




