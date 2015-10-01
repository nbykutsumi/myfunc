from numpy import *
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def DrawMap(a2in, a1lat, a1lon, BBox=[[-90., 0.],[90., 360.]], vmin=False, vmax=False, figname="./temp.png",stitle=False, parallels=arange(-90,90+0.1, 10), meridians=arange(0,360+0.1,10) ):
  # Lat, Lon ------
  a1lat = array( a1lat )
  a1lon = array( a1lon )
  a1LAT = r_[ array([-90.0]), (a1lat[1:] + a1lat[:-1])*0.5, array([90.0 ])]
  a1LON = r_[ array([0.0]),   (a1lon[1:] + a1lon[:-1])*0.5, array([360.0])]

  X,Y   = meshgrid(a1LON, a1LAT)
  # BBox --------
  [lllat,lllon],[urlat,urlon] = BBox

  # vmax, vmin --
  if type(vmax) == bool:
    vmax = a2in.max()
  if type(vmin) == bool:
    vmin = a2in.min()

  # Draw Map ----
  fig  = plt.figure()
  ax   = fig.add_axes([0.1,0.1,0.8,0.8])
  
  #M    = Basemap( resolution="l", llcrnrlat = lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=ax)
  M    = Basemap( resolution="h", llcrnrlat = lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=ax)
  #im   = M.pcolormesh(X,Y,a2in)
  im   = M.pcolormesh(X,Y,a2in, vmin=vmin, vmax=vmax)

  # coastline ---
  M.drawcoastlines()

  # meridians and parrallels -
  if type(parallels) != bool:
    M.drawparallels(parallels, labels=[1,0,0,0], fontsize=12, linewidth=1)
  if type(meridians) != bool:
    M.drawparallels(parallels, labels=[1,0,0,0], fontsize=12, linewidth=1)
  M.drawmeridians(meridians, labels=[0,0,0,1], fontsize=12, linewidth=1)

  # title -------
  if type(stitle) != bool:
    ax.set_title("%s"%(stitle))

  # colorbar ----
  plt.colorbar(im)

  # Save -------------
  plt.savefig(figname)
  print figname
