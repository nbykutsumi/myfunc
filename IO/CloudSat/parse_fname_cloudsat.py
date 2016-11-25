#! /usr/bin/python
#--------------------------------------------------------------
# CREATED BY : N.Utsumi
# BASED ON   : GPyM module by hjkim
#--------------------------------------------------------------
import    os,sys
from      datetime   import datetime, timedelta

def parse_fname_cloudsat(fName, ATTR):
    '''
    fName    : HDF file path
    ATTR     : list of attribtutes (i.e., 'sDTime' and/or 'eDTme')
    '''

    fName   = fName.split("_")
    sDTime  = datetime.strptime(fName[0], '%Y%j%H%M%S')
    offset  = timedelta(seconds=6000)   # 100 minutes

    dictFunc= {'sDTime': sDTime,
               'eDTime': sDTime+offset,
              }
    return [dictFunc[attr] for attr in ATTR]
