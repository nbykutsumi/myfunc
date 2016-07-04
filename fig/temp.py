from numpy import *
from bisect import bisect


#********************************************************
def lon2x(a1lon, lon):
  i = bisect(a1lon, lon)
  if i==0:
    x = i
  elif i == len(a1lon):
    x = i-1
  else:
    if   ( lon < (a1lon[i-1]+a1lon[i])*0.5 ):
      x = i-1
    else:
      x = i
  return x


a1lon = arange(10)
print a1lon
lon = 10
i = lon2x(a1lon, lon)
print lon, i
