from numpy import *
from bisect import bisect, bisect_left, bisect_right
import numpy as np
import numpy.ma as ma
import sys

def unfold2d( aSrc ):
    '''
    * unfold sub-domains
    from div_domain.py of CoreFrame, by H.Kim @ IIS, Univ. of Tokyo
    '''

    shape       = np.array( aSrc.shape, 'int' )
    outershp    = shape[-2:]
    innershp    = shape[:-2]

    nY          = outershp[0] * innershp[-2]
    nX          = outershp[1] * innershp[-1]

    toshape     = innershp[:-2].tolist() + [nY, nX]
    transAxis   = np.array( [0,2,1,3], 'int' )


    if len( shape ) > 2:

        additionalaxes  = list(range( len(shape)-4))

        transAxis       = ( transAxis + len(additionalaxes) ).tolist()
        idx             = 0

        for i in additionalaxes[::-1]:
            transAxis.insert(idx, i)


    return aSrc.transpose(*transAxis).reshape(*toshape)


def fold2d( aSrc, bndShp ):
    '''
    * divide n-dimensional map into small rectagular domains
    from div_domain.py of CoreFrame, by H.Kim @ IIS, Univ. of Tokyo

    aSrc    : input ndarray
    bndShp  : sub-domain shape

    ex) fold2d( ar(t,180,360), (90,180) ).shape   = (t, 2, 2,   90, 180)
        fold2d( ar(t,180,360), ( 2,  2) ).shape   = (t, 90,180, 2,  2)
    '''

    shape       = np.array( aSrc.shape, 'int' )
    outershp    = np.array( bndShp, 'int' )
    innershp    = shape[-len(outershp):] / outershp

    transAxis   = np.array( [0,2,1,3], 'int' )

    if len( shape ) > 2:

        additionalaxes  = list(range( len(shape) - 2))

        transAxis       = ( transAxis + len(additionalaxes) ).tolist()
        idx             = 0

        for i in additionalaxes[::-1]:
            transAxis.insert(idx, i)

    toshape     = shape[:-len(outershp)].tolist()   \
                + [outershp[0], innershp[0], outershp[1], innershp[1]]


    return aSrc.reshape( *toshape ).transpose( *transAxis )


def karnel_pooling_map2D_global(ain, dy, dx, func=None, miss_in=-9999, miss_out=-9999, cover_poles=True):
    ny,nx = ain.shape
    ny_large, nx_large = ny+2*dy, nx+2*dx
    ndup =  (2*dy+1)*(2*dx+1) # number of duplication
  
    if type(ain) is np.ma.core.MaskedArray: 
        ain   = ain.filled(miss_in)

    ain_large = expand_map_global_2d(ain, dy, dx, cover_poles=True)

    a3tmp = np.full((ndup,ny_large,nx_large),miss_in, dtype=ain.dtype)

    ldyx = [[y,x] for y in range(-dy,dy+1)
                  for x in range(-dx,dx+1)]

    for idup, (idy,idx) in enumerate(ldyx):
        a3tmp[idup] = shift_map_global(ain_large, idy, idx, miss_in)

    a3tmp = ma.masked_equal(a3tmp, miss_in)

    if func =='sum':
        a2out = a3tmp.sum(axis=0)
    elif func=='mean':
        a2out = a3tmp.mean(axis=0)
    elif func=='max':
        a2out = a3tmp.max(axis=0)
    elif func=='min':
        a2out = a3tmp.min(axis=0)
    else:
        print('check func', func)
        sys.exit()

    a2out = a2out.filled(miss_out)[dy:-dy,dx:-dx]
    return a2out




#def karnel_pooling_map2D_global(ain, dy, dx, func=None, miss_in=-9999, miss_out=-9999):
#    ny,nx = ain.shape
#    ndup =  (2*dy+1)*(2*dx+1) # number of duplication
#  
#    if type(ain) is np.ma.core.MaskedArray: 
#        ain   = ain.filled(miss_in)
#    a3tmp = np.full((ndup,ny,nx),miss_in, dtype=ain.dtype)
#
#    ldyx = [[y,x] for y in range(-dy,dy+1)
#                  for x in range(-dx,dx+1)]
#
#    for idup, (idy,idx) in enumerate(ldyx):
#        a3tmp[idup] = shift_map_global(ain, idy, idx, miss_in)
#
#    a3tmp = ma.masked_equal(a3tmp, miss_in)
#
#    if func =='sum':
#        a2out = a3tmp.sum(axis=0)
#    elif func=='mean':
#        a2out = a3tmp.meam(axis=0)
#    elif func=='max':
#        a2out = a3tmp.max(axis=0)
#    elif func=='min':
#        a2out = a3tmp.min(axis=0)
#
#
#    a2out = a2out.filled(miss_out)
#    return a2out

def shift_map_global(a2in, dy, dx, miss):
    aout = np.roll(a2in, shift=(dy, dx), axis=(0,1))
    if dy>0:
        aout[:dy] = miss
    elif dy<0:
        aout[dy:] = miss    

    return aout.astype(a2in.dtype)

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

def expand_map_global_2d(a2in, dy,dx, cover_poles=True):
    '''
    expand global map
    input shape (ny,nx)
    output shape: (ny+2dy, nx+2dx)
    '''
    ny,nx = a2in.shape
     
    #-- Make output array   --
    a2out = np.empty([ny+2*dy, nx+2*dx]).astype(a2in.dtype)

    #-- Fill center box -----
    a2out[dy:dy+ny, dx:dx+nx] = a2in

    #-- Latitude direction --
    if cover_poles==True:
        a2out[:dy,dx:dx+nx]  = np.flipud(np.roll(a2in[1:1+dy,:],  int(0.5*nx), axis=1))
        a2out[-dy:,dx:dx+nx] = np.flipud(np.roll(a2in[-dy-1:-1,:], int(0.5*nx), axis=1))

    else:
        a2out[:dy,dx:dx+nx]  = np.flipud(np.roll(a2in[:dy,:],  int(0.5*nx), axis=1))
        a2out[-dy:,dx:dx+nx] = np.flipud(np.roll(a2in[-dy:,:], int(0.5*nx), axis=1))

    #-- Longitude direction (wrap) --
    a2out[:, :dx]  = a2out[:,-2*dx:-dx]
    a2out[:, -dx:] = a2out[:,dx:2*dx]


    return a2out.astype(a2in.dtype)

#def shift_map(a2in, dy, dx, miss):
#    ny, nx = a2in.shape
#    a2out  = ones([ny,nx])*miss
#
#    if dy>=0:
#        if dx==0:
#            a2out[dy:,:] = a2in[:ny-dy,:]
#        else:
#            a2out[dy:,dx:] = a2in[:ny-dy,:-dx]
#            a2out[dy:,:dx] = a2in[:ny-dy,-dx:]
#
#    else:
#        if dx==0:
#            a2out[:dy,:] = a2in[-dy:,:]
#        else:
#            a2out[:dy,dx:] = a2in[-dy:,:-dx]
#            a2out[:dy,:dx] = a2in[-dy:,-dx:]
#
#    return a2out

     
