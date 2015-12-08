from numpy import *
from grids import *

def biIntp(Lat,Lon,z,LAT,LON,miss=-999):
    #***********************
    # biIntp
    # by hjkim, modified by N.Utsumi
    #***********************
    #nProc   = MP.cpu_count() if mp==True else 1

    #if type(mp) == int: nProc = mp

    #nProc   = settings.MAX_PROC if nProc > settings.MAX_PROC else nProc


    if Lat[1]>Lat[0] and LAT[1]>LAT[0]:     # in & out : -89.5 ~ 89.5
        sliceInLat  = None
        sliceOutLat = None
        sliceInZ    = None
        sliceOutZ   = None

    elif Lat[0]>Lat[1] and (LAT[0]>LAT[1]): # in & out :  89.5 ~ -89.5
        sliceInLat  = -1
        sliceOutLat = -1
        sliceInZ    = -1
        sliceOutZ   = -1

    elif Lat[0]>Lat[1] and (LAT[1]>LAT[0]): # in 89.5 ~ -89.5, out : -89.5 ~ 89.5
        sliceInLat  = -1
        sliceOutLat = None
        sliceInZ    = -1
        sliceOutZ   = None

    elif Lat[1]>Lat[0] and (LAT[0]>LAT[1]): # in -89.5 ~ 89.5, out : 89.5 ~ -89.5
        sliceInLat  = None
        sliceOutLat = -1
        sliceInZ    = None
        sliceOutZ   = -1

    else:
        raise ValueError,'coord mismatch!!'

    return gridsintp(
                     Lon,Lat[::sliceInLat],
                     z[::sliceInZ].T,
                     LON,LAT[::sliceOutLat],miss
                     ).T[...,::sliceOutZ,:]

