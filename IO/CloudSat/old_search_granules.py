#! /usr/bin/python
#--------------------------------------------------------------
# CREATED BY : N.Utsumi
# BASED ON   : GPyM module by hjkim
#--------------------------------------------------------------
import   os,sys
from     numpy           import arange, ma
from     collections     import deque
from     get_path        import get_path
from     get_gtrack_dim  import get_gtrack_dim

class SearchGranules( object ):
    def search_granules(self, srcDir, sDTime, eDTime, BBox=[[-90,-180],[90,180]],  verbose=True):
        '''
        BBox    : [[lllat,lllon], [urlat,urlon]]    /* lat: -90 ~ 90 */
                                                    /* lon: -180 ~ 180 */
        '''
        srcPATH = get_path(srcDir, sDTime, eDTime)
        if len(srcPATH)==0:
            print "!"*50
            print "Warning     by %s"%(__file__.split("/")[-1])
            print "No file for the time [%s]-[%s]"%(sDTime,eDTime)
            print "in %s"%(srcDir)
            print "!"*50
            raise IOError
        '''
        gtrkDim = [get_gtrack_dim(path, self.func_read, self.cached, self.cacheDir)
                           for path in srcPATH]
        '''
        gtrkDim = [get_gtrack_dim(path, self.func_read_vs, self.cached, self.cacheDir, verbose=verbose)
                           for path in srcPATH]

        DTime, Lat, Lon   = zip(*gtrkDim)
        Granule           = deque([])
        for dtime, lat, lon, path in map(None, DTime, Lat, Lon, srcPATH):

            mskLat  = ma.masked_outside( lat, BBox[0][0], BBox[1][0] ).mask
            mskLon  = ma.masked_outside( lon, BBox[0][1], BBox[1][1] ).mask
            mskTime = ma.masked_outside( dtime, sDTime, eDTime).mask

            #mask    = (mskLat + mskLon).all(1) + mskTime
            mask    = (mskLat + mskLon).all(0) + mskTime

            if not mask.all():
                idx = ma.array( arange(dtime.size), "int", mask=mask).compressed()
                Granule.append([path,
                                dtime[idx],
                                lat[idx],
                                lon[idx],
                                idx
                                ])
                if verbose==True:
                    print '* [V] ground track dimension (%s): %s'%(self.cached,path)
            else:
                if verbose==False:
                    print '* [_] ground track dimension (%s): %s'%(self.cached,path)

        summary = '| [{}] granules intersects domain {} out of [{}] total between ({}-{}) |\n'    \
                  .format( len(Granule), tuple(BBox), len(srcPATH), sDTime, eDTime )

        line    = '+' + '-'*len(summary[3:]) + '+\n'

        print line + summary + line

        return list(Granule)


