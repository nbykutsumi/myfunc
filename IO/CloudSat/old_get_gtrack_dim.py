#! /usr/bin/python
#--------------------------------------------------------------
# CREATED BY : N.Utsumi
# BASED ON   : GPyM module by hjkim
#--------------------------------------------------------------
import   os, sys
from     datetime       import datetime, timedelta
from     numpy          import array

from     alien.collection     import cached

#from     get_location   import get_location
from     get_location_cloudsat   import get_location
#from     get_dtime           import get_dtime
from     get_dtime_cloudsat  import get_dtime

def get_gtrack_dim(srcPath, fn_read, cache=False, cache_dir=None, verbose=True):
    '''
    scan granules and return dimension (T,Y,X) or ground tracks

    cache  : mode of cf.devel.collection.cached
              ['cached', 'cached-verbose', 'skip', 'update']
    '''
    '''
    verbose    = False if 'verbose' in cache \
            else True
    '''

    verbose    = verbose    # ??

#    prjName, .....
    PrdLong, yyyy, jjj, srcFName =  srcPath.split(os.path.sep)[-4:]

    print '+ Get Groundtrack Dimension: {}'.format( srcPath)

    cache_dir  = os.path.join( cache_dir, yyyy, jjj )

    Lat, Lon   = cached( srcFName + '.latlon',
                         cache_dir,
                         mode=cache,
                         verbose=verbose )(get_location)(srcPath, fn_read)

    '''
    Timetuple  = cached( srcFName + '.timetuple',
                         cache_dir,
                         mode=cache,
                         verbose=verbose )(get_dtime   )(srcPath, fn_read)
    '''
    DTime     = cached( srcFName + '.timetuple',
                         cache_dir,
                         mode=cache,
                         verbose=verbose )(get_dtime   )(srcPath, fn_read)

    '''
    # exception handling for us 1000000 instead of 0 ------------------------------------
    DTime   = []
    for y,m,d,H,M,S,uS in Timetuple:

        if uS == 1000000:
            DTime.append( datetime(y,m,d,H,M,S,0)+timedelta(seconds=1) )
            print 'Warning [Millisecond] == 1000 : %i %i %i %i %i %i %i'    \
                  %(y,m,d,H,M,S,uS/1000)

        else:
            DTime.append( datetime(y,m,d,H,M,S,uS) )
    # -----------------------------------------------------------------------------------
    '''

    #DTime   = array( DTime )
    return DTime, Lat, Lon
