#! /usr/bin/python
#--------------------------------------------------------------
# CREATED BY : N.Utsumi
# BASED ON   : GPyM module by hjkim
#--------------------------------------------------------------

import  os,sys
from    numpy      import array

def get_dtime(srcPath, func_read):
    Year    = func_read( srcPath, 'Year'        ).astype('int')
    Month   = func_read( srcPath, 'Month'       ).astype('int')
    Day     = func_read( srcPath, 'DayOfMonth'  ).astype('int')
    Hour    = func_read( srcPath, 'Hour'        ).astype('int')
    Minute  = func_read( srcPath, 'Minute'      ).astype('int')
    Second  = func_read( srcPath, 'Second'      ).astype('int')
    MicSec  = func_read( srcPath, 'MilliSecond' ).astype('int')*1000

    return array( [Year, Month, Day, Hour, Minute, Second, MicSec] ).T

