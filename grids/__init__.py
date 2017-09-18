from numpy import *
from bisect import bisect, bisect_left, bisect_right

def shift_map(a2in, dy, dx, miss):
    ny, nx = a2in.shape
    a2out  = ones([ny,nx])*miss

    if dy>=0:
        if dx==0:
            a2out[dy:,:] = a2in[:ny-dy,:]
        else:
            a2out[dy:,dx:] = a2in[:ny-dy,:-dx]
            a2out[dy:,:dx] = a2in[:ny-dy,-dx:]

    else:
        if dx==0:
            a2out[:dy,:] = a2in[-dy:,:]
        else:
            a2out[:dy,dx:] = a2in[-dy:,:-dx]
            a2out[:dy,:dx] = a2in[-dy:,-dx:]

    return a2out


def mk_mask_BBox(a1lat, a1lon, BBox, miss=0):
    """
    Only for global map
    """

    [[lat_min, lon_min],[lat_max, lon_max]] = BBox
    dlon      = (a1lon[1] - a1lon[0])
    dlat      = (a1lat[1] - a1lat[0])
    lon_first = a1lon[0] - 0.5*dlon
    lat_first = a1lat[0] - 0.5*dlat
    lon_last  = a1lon[-1] + 0.5*dlon
    lat_last  = a1lat[-1] + 0.5*dlat

    #--- xmin ----------
    if (lon_first <= lon_min):
        if (lon_min <= lon_last):
            xmin = bisect_right(a1lon+0.5*dlon, lon_min)
        else:
            xmin = bisect_right(a1lon+0.5*dlon, lon_min-lon_last)
    else:
        xmin = bisect_right(a1lon+0.5*dlon, lon_min+lon_last)

    #--- xmax ----------
    if (lon_first <= lon_max):
        if (lon_max <= lon_last):
            xmax = bisect_left(a1lon+0.5*dlon, lon_max)
        else:
            xmax = bisect_left(a1lon+0.5*dlon, lon_max-lon_last)
            
    else:
        xmax = bisect_left(a1lon+0.5*dlon, lon_max+lon_last)

    #--- ymin ----------
    ymin = bisect_right(a1lat+0.5*dlat, lat_min)

    #--- ymax ----------
    ymax = bisect_left(a1lat+0.5*dlat, lat_max)

    ##-----------
    ny = len(a1lat)
    nx = len(a1lon)
    a2regionmask  = ones(nx*ny).reshape(ny, nx)*miss

    if ( xmax < xmin):
        a2regionmask[ymin:ymax+1, xmin: nx] = 1.0
        a2regionmask[ymin:ymax+1, 0:xmax+1] = 1.0
    else:
        a2regionmask[ymin:ymax+1, xmin: xmax+1] = 1.0
    return a2regionmask


      
