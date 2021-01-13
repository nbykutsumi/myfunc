# %%
import numpy as np
from numpy import ma
#%matplotlib inline
from myfunc.grids import shift_map_global, karnel_pooling_map2D_global

miss = -9999
dy = 1
dx = 1
func = 'min'
miss_in = 0
miss_out= 9999
ain =np.arange(5*5).reshape(5,5)

#def karnel_pooling_map2D_global(ain, dy, dx, miss_in, miss_out):
#    ny,nx = ain.shape
#    ndup =  (2*dy+1)*(2*dx+1) # number of duplication
#    a3tmp = np.full((ndup,ny,nx),miss_in)
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
#    a2out = a2out.filled(miss_out)
#    return a2out


b= karnel_pooling_map2D_global(ain, dy,dx, func, miss_in, miss_out)
print ain
print ''
print b
# %%


# %%
