import  sys, os, importlib
import  socket
import  glob
from    numpy        import *
from    pyhdf        import SD
from    ConfigParser import SafeConfigParser

class L2A23(object):
    def __init__(self, version="07"):
        self.sensor  = "TRMM.PR"
        self.prdName = "L2A23"
        self.version = version


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


    def load_var_granule(self,srcPath,Var):
        aOut    = self.func_read(srcPath, Var, Slice=None, verbose=True)
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







