#! /usr/bin/python
#--------------------------------------------------------------
# CREATED BY : N.Utsumi
# BASED ON   : GPyM module by hjkim
#--------------------------------------------------------------
import    os,sys
from      fnmatch                 import filter
from      parse_fname_cloudsat    import parse_fname_cloudsat
from      datetime                import timedelta
from      collections             import deque

parse_fname = parse_fname_cloudsat

def get_path(srcDir, sDTime, eDTime):
    '''
    select CloudSAT(hdf4) files and return their paths
    '''
  
    LevName, prdVer = srcDir.split(os.path.sep)[-1].split(".")
    prdLv, prdName  = LevName.split("-")
  
    if sDTime == eDTime:
        raise ValueError, '%s == %s'%(sDTime, eDTime)
  
    total_days = (eDTime - sDTime).days
    
    lDTime  =  [sDTime + timedelta(days=i)
                for i in range((eDTime - sDTime).days +1)]
  
    # The first 100-min data may be included in the granule in a day before.  
    if sDTime.hour <2:
      lDTime = [sDTime - timedelta(days=1)] + lDTime

    
    srcDIR  = [os.path.join(srcDir, str(DTime.year), '%03d'%DTime.timetuple().tm_yday)
                   for DTime in lDTime]

    srcPATH = deque([])
    
    for srcDir in srcDIR:
        if not os.path.exists(srcDir):
            print "Warning [%s] directory does not exists!"%(srcDir)
            continue
    
        for srcFName in sorted( filter(os.listdir(srcDir), "*.hdf" )):
            sdt_gtrk, edt_gtrk  = parse_fname( srcFName, ['sDTime','eDTime'] )
            if sDTime <= edt_gtrk and eDTime >= sdt_gtrk:
                srcPATH.append( os.path.join(srcDir, srcFName) )
            else:
                continue

    return list(srcPATH) 
