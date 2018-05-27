#! /usr/bin/python
#--------------------------------------------------------------
# CREATED BY : N.Utsumi
# BASED ON   : GPyM module by hjkim
#--------------------------------------------------------------
import   os, sys, importlib
import   numpy as np

from    optparse        import OptionParser
from    ConfigParser    import SafeConfigParser
from    bisect          import bisect_left, bisect_right
from    collections     import deque

from    numpy           import empty, array, shape, ma

from    alien.dtrange               import dtrange

from    alien.GridCoordinates       import GridCoordinates

from    alien.TimeSeries            import bin_bytbound

from     cloudsat_data              import CloudSat_data
from     search_granules            import SearchGranules

from     resolve_cloudscenario      import Resolve_CloudScenario

class CloudSat( SearchGranules ):
    def __init__(self, prdLv, prdName, prdVer, **kwargs):
        """
        prdLev    : e.g.) '2B'
        prdName   : e.g.) 'CLDCLASS'
        prdVer    : e.g.) 'P_R04'
        """

        self.cfg        = SafeConfigParser( os.environ )
        self.cfg.read("/".join(__file__.split("/")[:-1]) + "/config")
        self.cfg._sections['Defaults'].update( kwargs )

        if self.cfg.get( "Defaults","dataroot") == "":
            self.cfg.set("Defaults","dataroot", os.environ["PWD"])

        self.dataDir    = self.cfg.get("Defaults","dataroot")
        self.prdName    = prdName
        self.prdLv      = prdLv
        self.prdVer     = prdVer

        self.nbin       = 125   # number of vertical bin
        self.prdDir     = os.path.join( self.dataDir,
                                        "%s-%s.%s"%(
                                        self.prdLv,
                                        self.prdName,
                                        self.prdVer))

        self.cached     = self.cfg.get("Defaults", "cached")
        self.cacheDir   = os.path.join(self.cfg.get("Defaults", "cache_dir"),
                                        "%s-%s.%s"%(
                                        self.prdLv,
                                        self.prdName,
                                        self.prdVer))

        fnPath          = self.cfg.get("Defaults","hdf4_module")
        fnName          = fnPath.split(".")[-1]
        modPath         = ".".join( fnPath.split(".")[:-1] )
        self.func_read  = getattr( importlib.import_module( modPath), fnName)


        fnPath          = self.cfg.get("Defaults","hdf4_vs_module")
        fnName          = fnPath.split(".")[-1]
        modPath         = ".".join( fnPath.split(".")[:-1] )
        self.func_read_vs  = getattr( importlib.import_module( modPath), fnName)

        self.Resolve_CloudScenario = Resolve_CloudScenario


    def __call__(self, varName, sDTime, eDTime, BBox=None, res=None, delT=None, verbose=True):
        '''
        res     : spa. res. of 2d-array   # not in service
        sDTime  : DTime bound left
        eDTime  : DTime bound right
        '''

        csData    = CloudSat_data()

        srcDir    = os.path.join( self.dataDir, 
                                  "%s-%s.%s"%(
                                   self.prdLv,
                                   self.prdName,
                                   self.prdVer) )

        assert os.path.exists( srcDir ), "{} is not exists.".format( srcDir)

        try:
          Granule   = self.search_granules( srcDir, sDTime, eDTime, BBox , verbose)
        except IOError:
          print "No granule    by %s"%(__file__.split("/")[-1])
          raise IOError

        nbin      = self.nbin
        #outSize   = sum( [ len(gra[2]) for gra in Granule ] ), Granule[0][2].shape[1], nbin
        #outSize   = sum( [ len(gra[2]) for gra in Granule ] ), nbin
        #Lat       = empty( outSize[:-1], "float32")
        #Lon       = empty( outSize[:-1], "float32")
        #aOut      = empty( outSize,      "float32")
        #DTime     = empty( outSize[:-1], "object" )

        Lat       = deque([]) 
        Lon       = deque([]) 
        aOut      = deque([]) 
        DTime     = deque([]) 

        #prvI      = 0
        for granule in Granule:
            srcPath, dtime, lat, lon, idx   = granule

            '''
            csData.srcPath.append(srcPath)
            csData.recLen.append( len(dtime) )    # number of data record for each file

            nxtI        = prvI + len(dtime)

            aOut[prvI:nxtI] = self.func_read( srcPath, varName, idx.tolist() )
            Lat[prvI:nxtI]  = lat 
            Lon[prvI:nxtI]  = lon
            DTime[prvI:nxtI]= dtime

            """
            if res != None and delT == None:
                csData.griddata.append( granule2map( lat, lon, aOut[prvI:nxtI], BBox, res ) )
                gpmData.grid    = GridCoordinates(mapCode, BBox=BBox)
            """

            prvI  = nxtI
            '''

            mskLat = ma.masked_inside( lat, BBox[0][0], BBox[1][0] ).mask
            mskLon = ma.masked_inside( lon, BBox[0][1], BBox[1][1] ).mask
            msk    = mskLat * mskLon


            if type(msk)== np.bool_:  # if msk == False
              msk = array([False]*len(lat))

            Lat  .extend(lat  [msk])
            Lon  .extend(lon  [msk])
            aOut .extend(self.func_read( srcPath, varName, idx.tolist() )[msk,:])

            dtime  = dtime[msk]
            DTime.extend(dtime)

            csData.srcPath.append(srcPath)
            csData.recLen.append( len(dtime) )    # number of data record for each file


        # Time binning
        if delT != None:
            dtBnd  = dtrange(sDTime, eDTime, delT)
        else:
            dtBnd  = [sDTime, eDTime]

        csData.dtime   = bin_bytbound( DTime, dtBnd, array(DTime) )
        csData.lat     = bin_bytbound( DTime, dtBnd, array(Lat  ) )
        csData.lon     = bin_bytbound( DTime, dtBnd, array(Lon  ) )
        csData.data    = bin_bytbound( DTime, dtBnd, array(aOut ) )

        return csData
