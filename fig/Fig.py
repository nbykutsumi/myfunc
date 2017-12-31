i
port matplotlib
matplotlib.use("Agg")
from numpy import *
from myfunc.fig import BoundaryNorm, BoundaryNormSymm
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.basemap import Basemap
from bisect import bisect
#********************************************************
def lon2ixpy(a1lon, lon):
  i = bisect(a1lon, lon)
  if i==0:
    ix = i
  elif i == len(a1lon):
    ix = i-1
  else:
    if   ( lon < (a1lon[i-1]+a1lon[i])*0.5 ):
      ix = i-1
    else:
      ix = i
  return ix

#********************************************************
def lat2iypy(a1lat, lat):
  i = bisect(a1lat, lat)
  if i==0:
    iy = i
  elif i == len(a1lat):
    iy = i-1
  else:
    if   ( lat < (a1lat[i-1]+a1lat[i])*0.5 ):
      iy = i-1
    else:
      iy = i
  return iy


#********************************************************
def DrawMap(a2in, a1lat, a1lon, BBox=[[-90.,0],[90.,360]], bnd=False, symm=True, lowest_white=True, mycm="jet", figname="./temp.png", stitle=False, titlefontsize=8, cbarname=False, miss=-9999.0, a2shade=False, coef=1.0, lonlatfontsize=10.0, lonrotation=0, ticks=None, gridlinewidth=1.0,figsize=False):
  #-- prep ----------------
  plt.clf()

  # Lat, Lon ------
  a1lat = array( a1lat )
  a1lon = array( a1lon )

  latmin = a1lat[0]  - (a1lat[1]  - a1lat[0])*0.5
  latmax = a1lat[-1] + (a1lat[-1] - a1lat[-2])*0.5
  lonmin = a1lon[0]  - (a1lon[1]  - a1lon[0])*0.5
  lonmax = a1lon[-1] + (a1lon[-1] - a1lon[-2])*0.5

  a1LAT = r_[ array([latmin]), (a1lat[1:] + a1lat[:-1])*0.5, array([latmax])]
  a1LON = r_[ array([lonmin]),   (a1lon[1:] + a1lon[:-1])*0.5, array([lonmax])]

  X,Y   = meshgrid(a1LON, a1LAT)
  # BBox --------
  [lllat,lllon],[urlat,urlon] = BBox

  #------------------------
  # coef
  #------------------------
  a2in = (ma.masked_equal(a2in, miss)*coef)

  #------------------------
  # Basemap
  #------------------------
  # e.g. figsize = (3,3)
  if figsize == False:
    figmap   = plt.figure()
  else:
    figmap   = plt.figure(figsize=figsize)
  #----------
  axmap    = figmap.add_axes([0.15, 0.1, 0.8, 0.75])
  #----------
  M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)

  #-- color ---------------
  if (type(bnd) != bool):
    if symm == True:
      #-- for symm -----------
      cminst   = matplotlib.cm.get_cmap(mycm, len(bnd)+1)
      acm      = cminst( arange( len(bnd)+1 ) )
      #-- for  lowest white --
      if lowest_white ==True:
        acm[0] = [1,1,1,1]
      #----------------------- 
      lcm      = acm.tolist()
      mycm     = matplotlib.colors.ListedColormap( lcm )
    else:
      mycm     = mycm

  #--- pcolormesh -----------
  if (type(bnd) != bool):
    if symm == True:
      im       = M.pcolormesh(X,Y,a2in, norm=BoundaryNormSymm(bnd), cmap=mycm)
    else:
      im       = M.pcolormesh(X,Y,a2in, norm=BoundaryNorm(bnd), cmap=mycm)
  else:
    im       = M.pcolormesh(X,Y,a2in, cmap=mycm)

  #-- colorbar for self -
  if cbarname == "self":
    plt.colorbar(im, ticks=ticks)

  #-- shade     -----------
  if type(a2shade) != bool:
    a2shade  = ma.masked_not_equal(a2shade, miss)
    cmshade  = matplotlib.colors.ListedColormap([(0.8,0.8,0.8), (0.8,0.8,0.8)])
    im       = M.pcolormesh(X,Y,a2shade, cmap=cmshade)

  #-- coastline ---------------
  M.drawcoastlines()

  #-- meridians and parallels
  parallels = arange(-90.,90,30.)
  M.drawparallels(parallels,labels=[1,0,0,0],fontsize=lonlatfontsize, linewidth=gridlinewidth)

  meridians = arange(0.,360.,30.)
  M.drawmeridians(meridians,labels=[0,0,0,1],fontsize=lonlatfontsize,rotation=lonrotation, linewidth=gridlinewidth)

  #-- title -------------------
  if stitle != False:
    axmap.set_title("%s"%(stitle), fontsize=titlefontsize)

  #-- save --------------------
  plt.savefig(figname)

  # for colorbar ---
  if (type(cbarname) ==bool)or(cbarname==None):
    pass
  elif cbarname == "self":
    pass
  else:
    plt.clf()
    figmap   = plt.figure()
    axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
    M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
    figcbar   = plt.figure(figsize=(5,0.6))
    axcbar    = figcbar.add_axes([0, 0.4, 1.0, 0.6])
    #----------
    if type(bnd) == bool:
      im       = M.imshow(a2in, origin="lower", cmap=mycm)
      plt.colorbar(im, extend="both", cax=axcbar, orientation="horizontal", ticks=ticks)
    else:
      im       = M.imshow(a2in, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm)
      bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
      plt.colorbar(im, boundaries= bnd_cbar, extend="both", cax=axcbar, orientation="horizontal", ticks=ticks)
    #----------
    figcbar.savefig(cbarname)
    print cbarname

#********************************************************
def DrawMapSimple(a2in, a1lat, a1lon, BBox=[[-90., 0.],[90., 360.]], bnd=False, vmin=False, vmax=False, cmap="Spectral", extend="neither", white_minmax="neither", figname="./temp.png", cbarname=False, stitle=False, parallels=arange(-90,90+0.1, 30), meridians=arange(-180,360+0.1,30) ,maskcolor=False, figsize=False):
  # Lat, Lon ------
  a1lat = array( a1lat )
  a1lon = array( a1lon )

  latmin = a1lat[0]  - (a1lat[1]  - a1lat[0])*0.5
  latmax = a1lat[-1] + (a1lat[-1] - a1lat[-2])*0.5
  lonmin = a1lon[0]  - (a1lon[1]  - a1lon[0])*0.5
  lonmax = a1lon[-1] + (a1lon[-1] - a1lon[-2])*0.5

  a1LAT = r_[ array([latmin]), (a1lat[1:] + a1lat[:-1])*0.5, array([latmax])]
  a1LON = r_[ array([lonmin]),   (a1lon[1:] + a1lon[:-1])*0.5, array([lonmax])]

  X,Y   = meshgrid(a1LON, a1LAT)
  # BBox --------
  [lllat,lllon],[urlat,urlon] = BBox

  # vmax, vmin --
  if type(vmax) == bool:
    vmax = a2in.max()
  if type(vmin) == bool:
    vmin = a2in.min()


  ##-- color ---------------
  if (type(bnd) != bool):
    bnd = list(bnd)

    if extend == "neither":
      bnd  = bnd
    elif extend == "both":
      bnd  = [-1.0e+40] + bnd + [1.0e+40]
    elif extend == "min":
      bnd  = [-1.0e+40] + bnd
    elif extend == "max":
      bnd  = bnd + [+1.0e+40]
    else:
      print "check extend", extend
      print __FILE__()
      sys.exit()

    cminst   = matplotlib.cm.get_cmap(cmap, len(bnd))
    acm      = cminst( arange( len(bnd)))
    lcm      = acm.tolist()
    cmap     = matplotlib.colors.ListedColormap( lcm )
    icent    = len(acm)/2 -1
    if   white_minmax=="min":
      acm[0]  =[1,1,1,1]
    elif white_minmax=="max":
      acm[-2] =[1,1,1,1]
    elif white_minmax=="both":
      acm[0]  =[1,1,1,1]
      acm[-2] =[1,1,1,1]
    elif white_minmax=="center":
      acm[icent] =[1,1,1,1]

    lcm      = acm.tolist()
    cmap     = matplotlib.colors.ListedColormap( lcm )



#    if extend == "neither":
#      cminst   = matplotlib.cm.get_cmap(cmap, len(bnd))
#      acm      = cminst( arange( len(bnd)))
#    elif extend == "both":
#      cminst   = matplotlib.cm.get_cmap(cmap, len(bnd)+2)
#      acm      = cminst( arange( len(bnd)+2 ))
#    elif extend in ["min","max"]:
#      cminst   = matplotlib.cm.get_cmap(cmap, len(bnd)+1)
#      acm      = cminst( arange( len(bnd)+1 ))
#
#    if   white_minmax=="min":
#      lcm      = [[1,1,1,1]]+ acm.tolist()[1:]
#    elif white_minmax=="max":
#      lcm      = acm.tolist()[:-1] + [[1,1,1,1]]
#    elif white_minmax=="both":
#      lcm      = [[1,1,1,1]] + acm.tolist()[1:-1] + [[1,1,1,1]]
#    elif white_minmax=="center":
#      icent    = len(acm)/2
#      print "*"*50
#      print "bnd=",bnd
#      print "acm=",acm
#      print len(acm)
#      print "incent",icent
#      acm[icent] =[1,1,1,1]
#      lcm      = acm.tolist()
#
#    else:
#      lcm      = acm.tolist()
#
#    cmap     = matplotlib.colors.ListedColormap( lcm )


  # BoundaryNorm
  if type(bnd) != bool:
    norm   = colors.BoundaryNorm(boundaries=bnd, ncolors=len(bnd)+1)
  else:
    norm   = None

  # Draw Map ----
  if figsize == False:
    fig  = plt.figure()
  else:
    fig  = plt.figure(figsize=figsize)

  # color for masked grids --
  if type(maskcolor) == bool:
    maskcolor = "w"
  else:
    maskcolor = maskcolor

  ax   = fig.add_axes([0.1,0.1,0.8,0.8], axisbg=maskcolor)
  
  M    = Basemap( resolution="l", llcrnrlat = lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=ax)
  im   = M.pcolormesh(X,Y,a2in, vmin=vmin, vmax=vmax, cmap=cmap, norm=norm)


  # coastline ---
  M.drawcoastlines()

  # meridians and parrallels -
  if type(parallels) != bool:
    M.drawparallels(parallels, labels=[1,0,0,0], fontsize=10, linewidth=1)
  if type(meridians) != bool:
    M.drawparallels(parallels, labels=[1,0,0,0], fontsize=10, linewidth=1)
  M.drawmeridians(meridians, labels=[0,0,0,1], fontsize=10, linewidth=1)

  # title -------
  if type(stitle) != bool:
    ax.set_title("%s"%(stitle))

  # Save -------------
  plt.savefig(figname)
  print figname

  # colorbar ----
  if type(cbarname) != bool:
    figcbar    = plt.figure(figsize=(5, 0.6))
    axcbar     = figcbar.add_axes([0.1,0.4,0.8,0.58])
    if type(bnd) != bool:
      boundaries = bnd
      plt.colorbar(im, boundaries=boundaries, extend=extend, cax=axcbar, orientation="horizontal")
    else:
      plt.colorbar(im, extend=extend, cax=axcbar, orientation="horizontal")
    figcbar.savefig(cbarname)
    print cbarname




##********************************************************
#def DrawMapSimple(a2in, a1lat, a1lon, BBox=[[-90., 0.],[90., 360.]], vmin=False, vmax=False, cmap="Spectral",figname="./temp.png",stitle=False, parallels=arange(-90,90+0.1, 30), meridians=arange(-180,360+0.1,30) ,maskcolor=False):
#  # Lat, Lon ------
#  a1lat = array( a1lat )
#  a1lon = array( a1lon )
#
#  latmin = a1lat[0]  - (a1lat[1]  - a1lat[0])*0.5
#  latmax = a1lat[-1] + (a1lat[-1] - a1lat[-2])*0.5
#  lonmin = a1lon[0]  - (a1lon[1]  - a1lon[0])*0.5
#  lonmax = a1lon[-1] + (a1lon[-1] - a1lon[-2])*0.5
#
#  a1LAT = r_[ array([latmin]), (a1lat[1:] + a1lat[:-1])*0.5, array([latmax])]
#  a1LON = r_[ array([lonmin]),   (a1lon[1:] + a1lon[:-1])*0.5, array([lonmax])]
#
#  X,Y   = meshgrid(a1LON, a1LAT)
#  # BBox --------
#  [lllat,lllon],[urlat,urlon] = BBox
#
#  # vmax, vmin --
#  if type(vmax) == bool:
#    vmax = a2in.max()
#  if type(vmin) == bool:
#    vmin = a2in.min()
#
#  # Draw Map ----
#  fig  = plt.figure()
#  # color for masked grids --
#  if type(maskcolor) == bool:
#    maskcolor = "w"
#  else:
#    maskcolor = maskcolor
#
#  ax   = fig.add_axes([0.1,0.1,0.8,0.8], axisbg=maskcolor)
#  
#  M    = Basemap( resolution="l", llcrnrlat = lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=ax)
#  im   = M.pcolormesh(X,Y,a2in, vmin=vmin, vmax=vmax, cmap=cmap)
#
#
#  # coastline ---
#  M.drawcoastlines()
#
#  # meridians and parrallels -
#  if type(parallels) != bool:
#    M.drawparallels(parallels, labels=[1,0,0,0], fontsize=10, linewidth=1)
#  if type(meridians) != bool:
#    M.drawparallels(parallels, labels=[1,0,0,0], fontsize=10, linewidth=1)
#  M.drawmeridians(meridians, labels=[0,0,0,1], fontsize=10, linewidth=1)
#
#  # title -------
#  if type(stitle) != bool:
#    ax.set_title("%s"%(stitle))
#
#  # colorbar ----
#  plt.colorbar(im, orientation="horizontal")
#
#  # Save -------------
#  plt.savefig(figname)
#  print figname
#

#********************************************************
def DrawVectorSimple(U, V, a1lat, a1lon, BBox=[[-90., 0.],[90., 360.]], figname="./temp.png",stitle=False, parallels=arange(-90,90+0.1, 30), meridians=arange(-180,360+0.1,30) ,maskcolor=False, scale=False, interval=False):

  # Lat, Lon ------
  a1lat = array( a1lat )
  a1lon = array( a1lon )

  latmin = a1lat[0]  - (a1lat[1]  - a1lat[0])*0.5
  latmax = a1lat[-1] + (a1lat[-1] - a1lat[-2])*0.5
  lonmin = a1lon[0]  - (a1lon[1]  - a1lon[0])*0.5
  lonmax = a1lon[-1] + (a1lon[-1] - a1lon[-2])*0.5

  a1LAT = r_[ array([latmin]), (a1lat[1:] + a1lat[:-1])*0.5, array([latmax])]
  a1LON = r_[ array([lonmin]),   (a1lon[1:] + a1lon[:-1])*0.5, array([lonmax])]

  X,Y   = meshgrid(a1LON, a1LAT)
  # BBox --------
  [lllat,lllon],[urlat,urlon] = BBox

  # scale  ------
  if type(scale) == bool:
    scale = (abs(U).mean() + abs(V).mean())*0.5 
    print "*"*50
    print scale

  # interval ---
  if type(interval) != bool:
    k  = interval
    X  = X[::k, ::k]
    Y  = Y[::k, ::k]
    U  = U[::k, ::k]
    V  = V[::k, ::k]

  # Draw Map ----
  fig  = plt.figure()
  # color for masked grids --
  if type(maskcolor) == bool:
    maskcolor = "w"
  else:
    maskcolor = maskcolor

  ax   = fig.add_axes([0.1,0.1,0.8,0.8], axisbg=maskcolor)
  
  M    = Basemap( resolution="l", llcrnrlat = lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=ax)
  im   = M.quiver(X, Y, U, V
                 ,units = "xy"
                 ,scale = scale
                 ,headwidth= scale*3
                 ,pivot = "mid"
                 )

  # coastline ---
  M.drawcoastlines()

  # meridians and parrallels -
  if type(parallels) != bool:
    M.drawparallels(parallels, labels=[1,0,0,0], fontsize=10, linewidth=1)
  if type(meridians) != bool:
    M.drawparallels(parallels, labels=[1,0,0,0], fontsize=10, linewidth=1)
  M.drawmeridians(meridians, labels=[0,0,0,1], fontsize=10, linewidth=1)

  # title -------
  if type(stitle) != bool:
    ax.set_title("%s"%(stitle))

  # Save -------------
  plt.savefig(figname)
  print figname



