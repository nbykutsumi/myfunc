import  sys, os, importlib
import  socket
import  glob
from    numpy        import *
from    alien        import read_hdf5
import  functions

class L2A_GPROF_HDF5(object):
    def __init__(self, sensor='TRMM.TMI', prdName='2A-CLIM',version='V05',minorversion='A'):
        self.sensor  = sensor
        self.prdName = prdName
        self.version = version
        self.fullversion= '%s%s'%(version, minorversion)


        self.hostname= socket.gethostname()
        if   self.hostname=="well":
            self.rootDir  = "/media/disk2/share/data/GPM"
        elif self.hostname=="mizu":
            self.rootDir  = "/home/utsumi/mnt/wellshare/data/GPM"
            #self.rootDir  = "/work/a01/utsumi/data/GPM"

        ## read_hdf function
        self.func_read  = read_hdf5.read_hdf5


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
        
        lPath  = glob.glob(srcDir+"/%s*.%s.HDF5"%(self.prdName, self.fullversion))
        return lPath

    def load_dtime_granule(self, srcPath=None):
        return functions.get_dtime_2AGPROF_hdf5(srcPath, self.load_var_granule)



if __name__ == '__main__':
    sensor = 'TRMM.TMI'
    prdName= '2A-CLIM'
    version= 'V05'
    minorversion='A'
    gpm = L2A_GPROF_HDF5(sensor, prdName, version, minorversion)

    srcDir = '/home/utsumi/mnt/wellshare/data/GPM/TRMM.TMI/2A-CLIM/V05/2014/10'
    srcPath= srcDir + '/2A-CLIM.TRMM.TMI.GPROF2017v2.20141031-S033854-E051057.096593.V05A.HDF5'

    #varName= 'GprofDHeadr/clusterProfiles'
    #varName= 'S1/profileTemp2mIndex'
    #varName= 'S1/profileNumber'
    #varName= 'S1/profileScale'
    varName= 'S1/ScanTime/Year'

    a = gpm.load_var_granule(srcPath=srcPath, Var=varName)

    print a
    print a.shape

    #lgranule = gpm.list_granule(2014,10)
    #print lgranule

    adtime   = gpm.load_dtime_granule(srcPath=srcPath)
    print adtime
