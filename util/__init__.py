from datetime import datetime, timedelta
import os

def mk_dir(sdir):
  try:
    os.makedirs(sdir)
  except OSError:
    pass

def ret_lDTime(iDTime,eDTime,dDTime):
  total_steps = int( (eDTime - iDTime).total_seconds() / dDTime.total_seconds() + 1 )
  return [iDTime + dDTime*i for i in range(total_steps)]

def ret_dMonName():
  return {1:"Jan",2:"Feb",3:"Mar",4 :"Apr",5 :"May",6 :"Jun"
         ,7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}

def ret_lYM(iYM, eYM):
  """
  iYM = [iYear, iMon], eYM = [eYear, eMon]
  """
  iYear, iMon = iYM
  eYear, eMon = eYM
  lYM = []
  for Year in range(iYear, eYear+1):
    if iYear == eYear:
      lMon = range(iMon,eMon+1)
    elif Year == iYear:
      lMon = range(iMon,12+1)
    elif Year == eYear:
      lMon = range(1,eMon+1)
    else:
      lMon = range(1,12+1)   

    for Mon in lMon:
      lYM.append([Year,Mon])
  return lYM 

def array2csv(a):
  if len(a.shape)==1:
    sout = "\n".join(map(str,a))
  elif len(a.shape)==2:
    lline = [",".join( map(str,line)) for line in a]
    sout  = "\n".join(lline).strip()
  return sout

def list2csv(a):
  if type(a[0]) !=list:
    sout = "\n".join(map(str,a))
  elif type(a[0]) ==list:
    lline = [",".join( map(str,line)) for line in a]
    sout  = "\n".join(lline).strip()
  return sout

