#! /usr/bin/python
#--------------------------------------------------------------
# CREATED BY : N.Utsumi
# BASED ON   : GPyM module by hjkim
#--------------------------------------------------------------

import  os,sys
from    numpy      import array
from    datetime   import datetime, timedelta

def get_dtime(srcPath, func_read):

    '''
    Seconds since the start of the granule for each profile. The first profile is 0. 
    '''
    pTIME   = func_read( srcPath, 'Profile_time')


    '''
    The UTC seconds since 00:00 Z of the first profile in the data file. 
    '''
    Year, DOY = map(int, srcPath.split("/")[-3:-1])
    sUTC      = func_read( srcPath, 'UTC_start'   )[0]
    sDTime    = datetime(Year,1,1,0) + timedelta(days=DOY-1)\
                                     + timedelta(seconds=sUTC)
    pDTime  =  sDTime + \
             + array([timedelta(seconds = sec) 
                              for sec in pTIME])


    #'''
    #The TAI timestamp for the first profile in the data file. TAI is International Atomic Time: 
    #seconds since 00:00:00 Jan 1 1993. 
    #'''
    #sTAI    = func_read( srcPath, 'TAI_start'   )[0]
    #sDTime  = datetime(1993,1,1,0,0,0) + timedelta(seconds=sTAI)
    #pDTime  =  sDTime + \
    #         + array([timedelta(seconds = sec) 
    #                          for sec in pTIME])


    '''
    Year    = func_read( srcPath, 'Year'        ).astype('int')
    Month   = func_read( srcPath, 'Month'       ).astype('int')
    Day     = func_read( srcPath, 'DayOfMonth'  ).astype('int')
    Hour    = func_read( srcPath, 'Hour'        ).astype('int')
    Minute  = func_read( srcPath, 'Minute'      ).astype('int')
    Second  = func_read( srcPath, 'Second'      ).astype('int')
    MicSec  = func_read( srcPath, 'MilliSecond' ).astype('int')*1000
    '''

    #return array( [Year, Month, Day, Hour, Minute, Second, MicSec] ).T
    return pDTime
