import  os, sys
from    numpy       import array, ma
from    datetime    import datetime, timedelta
import  h5py

def load_file_hdf5(srcPath):
    return h5py.File(srcPath, 'r')

def get_dtime_L2_DPR(srcPath=None, scan=None, func_read=None):
    # scan = 'NS' / 'MS' / 'HS'

    Year    = func_read( srcPath, scan + '/ScanTime/Year'        ).astype('int')
    Month   = func_read( srcPath, scan + '/ScanTime/Month'       ).astype('int')
    Day     = func_read( srcPath, scan + '/ScanTime/DayOfMonth'  ).astype('int')
    Hour    = func_read( srcPath, scan + '/ScanTime/Hour'        ).astype('int')
    Minute  = func_read( srcPath, scan + '/ScanTime/Minute'      ).astype('int')
    Second  = func_read( srcPath, scan + '/ScanTime/Second'      ).astype('int')
    MicSec  = func_read( srcPath, scan + '/ScanTime/MilliSecond' ).astype('int')*1000

    DTime   = []
    for y,m,d,H,M,S,uS in map(None,Year,Month,Day,Hour,Minute,Second,MicSec):

        if uS == 1000000:
            DTime.append( datetime(y,m,d,H,M,S,0)+timedelta(seconds=1) )
            print 'Warning [Millisecond] == 1000 : %i %i %i %i %i %i %i'%(y,m,d,H,M,S,uS/1000)

        elif S == 60:
            DTime.append( datetime(y,m,d,H,M,59,uS)+timedelta(seconds=1) )
            print 'Warning [Second] == 60 : %i %i %i %i %i %i %i'%(y,m,d,H,M,S,uS/1000)

        else:
            DTime.append( datetime(y,m,d,H,M,S,uS) )

    return array( DTime )

def get_dtime_L2_EPC_hdf5(srcPath, func_read):
    Year    = func_read( srcPath, 'S1/ScanTime/Year'        ).astype('int')
    Month   = func_read( srcPath, 'S1/ScanTime/Month'       ).astype('int')
    Day     = func_read( srcPath, 'S1/ScanTime/DayOfMonth'  ).astype('int')
    Hour    = func_read( srcPath, 'S1/ScanTime/Hour'        ).astype('int')
    Minute  = func_read( srcPath, 'S1/ScanTime/Minute'      ).astype('int')
    Second  = func_read( srcPath, 'S1/ScanTime/Second'      ).astype('int')
    MicSec  = func_read( srcPath, 'S1/ScanTime/MilliSecond' ).astype('int')*1000

    DTime   = []
    for y,m,d,H,M,S,uS in map(None,Year,Month,Day,Hour,Minute,Second,MicSec):

        if uS == 1000000:
            DTime.append( datetime(y,m,d,H,M,S,0)+timedelta(seconds=1) )
            print 'Warning [Millisecond] == 1000 : %i %i %i %i %i %i %i'%(y,m,d,H,M,S,uS/1000)

        elif S == 60:
            DTime.append( datetime(y,m,d,H,M,59,uS)+timedelta(seconds=1) )
            print 'Warning [Second] == 60 : %i %i %i %i %i %i %i'%(y,m,d,H,M,S,uS/1000)

        else:
            DTime.append( datetime(y,m,d,H,M,S,uS) )

    return array( DTime )

 



def get_dtime_2AGPROF_hdf5(srcPath, func_read):
    Year    = func_read( srcPath, 'S1/ScanTime/Year'        ).astype('int')
    Month   = func_read( srcPath, 'S1/ScanTime/Month'       ).astype('int')
    Day     = func_read( srcPath, 'S1/ScanTime/DayOfMonth'  ).astype('int')
    Hour    = func_read( srcPath, 'S1/ScanTime/Hour'        ).astype('int')
    Minute  = func_read( srcPath, 'S1/ScanTime/Minute'      ).astype('int')
    Second  = func_read( srcPath, 'S1/ScanTime/Second'      ).astype('int')
    MicSec  = func_read( srcPath, 'S1/ScanTime/MilliSecond' ).astype('int')*1000

    DTime   = []
    for y,m,d,H,M,S,uS in map(None,Year,Month,Day,Hour,Minute,Second,MicSec):

        if uS == 1000000:
            DTime.append( datetime(y,m,d,H,M,S,0)+timedelta(seconds=1) )
            print 'Warning [Millisecond] == 1000 : %i %i %i %i %i %i %i'%(y,m,d,H,M,S,uS/1000)

        elif S == 60:
            DTime.append( datetime(y,m,d,H,M,59,uS)+timedelta(seconds=1) )
            print 'Warning [Second] == 60 : %i %i %i %i %i %i %i'%(y,m,d,H,M,S,uS/1000)

        else:
            DTime.append( datetime(y,m,d,H,M,S,uS) )

    return array( DTime )

 

def get_dtime_trmm(srcPath, func_read):
    Year    = func_read( srcPath, 'Year'        ).astype('int')
    Month   = func_read( srcPath, 'Month'       ).astype('int')
    Day     = func_read( srcPath, 'DayOfMonth'  ).astype('int')
    Hour    = func_read( srcPath, 'Hour'        ).astype('int')
    Minute  = func_read( srcPath, 'Minute'      ).astype('int')
    Second  = func_read( srcPath, 'Second'      ).astype('int')
    MicSec  = func_read( srcPath, 'MilliSecond' ).astype('int')*1000

    DTime   = []
    for y,m,d,H,M,S,uS in map(None,Year,Month,Day,Hour,Minute,Second,MicSec):

        if uS == 1000000:
            DTime.append( datetime(y,m,d,H,M,S,0)+timedelta(seconds=1) )
            print 'Warning [Millisecond] == 1000 : %i %i %i %i %i %i %i'%(y,m,d,H,M,S,uS/1000)

        elif S == 60:
            DTime.append( datetime(y,m,d,H,M,59,uS)+timedelta(seconds=1) )
            print 'Warning [Second] == 60 : %i %i %i %i %i %i %i'%(y,m,d,H,M,S,uS/1000)

        else:
            DTime.append( datetime(y,m,d,H,M,S,uS) )

    return array( DTime )

 
def ret_extract_a1mask(Lat=None,Lon=None,dtime=None,BBox=None,sDTime=None,eDTime=None): 

    if type(Lat) !=bool:
        mskLat  = ma.masked_outside( Lat, BBox[0][0], BBox[1][0] ).mask
    else:
        mskLat  = False

    if type(Lon) !=bool:
        mskLon  = ma.masked_outside( Lon, BBox[0][1], BBox[1][1] ).mask
    else:
        mskLon  = False

    if type(dtime) !=bool:
        mskTime = ma.masked_outside( dtime, sDTime, eDTime).mask
    else:
        mskTime = False

    mask    = (mskLat + mskLon).all(1) + mskTime
    return mask


#******* copy functions ************
get_dtime_L1_GMI = get_dtime_L2_DPR

#***********************************


