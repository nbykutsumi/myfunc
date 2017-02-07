from numpy import *
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

def crop_map(a2in, a1lat, a1lon, BBox):
    lllat, lllon = BBox[0]
    urlat, urlon = BBox[1]

    dlat = a1lat[1] - a1lat[0]
    dlon = a1lon[1] - a1lon[0]

    iy = 
 
    if ((a1lon[0]-dlon <= lllon)&(urlon <= a1lon[-1]+dlon)):
        
