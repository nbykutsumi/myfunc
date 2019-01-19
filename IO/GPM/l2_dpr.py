import  sys, os, importlib
import  socket
import  glob
from    numpy        import *
from    alien        import read_hdf5
import  functions

class L2_DPR(object):
    def __init__(self, sensor='GPM.DPR', prdName='2A.DPR',version='05',minorversion='A',agency='NASA'):
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
        elif self.hostname=="shui":
            self.rootDir  = "/work/hk01/PMM/%s"%(agency)

        ## read_hdf function
        self.func_read  = read_hdf5.read_hdf5


    def load_var_granule(self,srcPath=None,Var=None,verbose=False):
        aOut    = self.func_read(srcPath, Var, Slice=None, verbose=verbose)
        return  aOut


    def list_granule(self, Year, Mon, Day):
        srcDir  = os.path.join(self.rootDir,\
                               self.sensor ,\
                               self.prdName,\
                               self.version,\
                               "%04d"%(Year),\
                               "%02d"%(Mon),\
                               "%02d"%(Day)\
                              )

        if agency=='JAXA':        
            lPath  = glob.glob(srcDir+"/*_%s.h5"%(self.fullversion))
        elif agency=='NASA':
            lPath  = glob.glob(srcDir+"/*.%s.HDF5"%(self.fullversion))
        else:
            print 'check agancy',agency
            sys.exit()
        return lPath

    def load_dtime_granule(self, srcPath=None, scan=None):
        ''' scan = "NS" / "MS" / "HS" '''
        return functions.get_dtime_L2_DPR(srcPath, scan, self.load_var_granule)



if __name__ == '__main__':
    sensor = 'GPM.DPR'
    prdName= '2A.DPR'
    version= '05'
    minorversion='A'
    gpm = L2_DPR(sensor, prdName, version, minorversion)

    srcDir = '/media/disk2/share/data/GPM/GPM.DPR/2A.DPR/05A/2017/12/01'
    srcPath= srcDir + '/GPMCOR_DPR_1712010002_0134_021350_L2S_DD2_05A.h5'

    #varName= 'NS/ScanTime/Year'
    varName= 'NS/SLV/precipRate'

    a = gpm.load_var_granule(srcPath=srcPath, Var=varName)

    print a
    print a.shape

    #lgranule = gpm.list_granule(2014,10)
    #print lgranule

    adtime   = gpm.load_dtime_granule(srcPath=srcPath, scan='NS')
    print adtime
