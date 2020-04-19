from numpy import *
import sys
import myfunc.util as util
from datetime import datetime, timedelta
from collections import deque

class GRDC(object):
    def __init__(self):
        self.miss_out = -9999.
        pass


    def mk_grdcDailyArray(self, srcPath, iDTimeOut, eDTimeOut, dattype='calc'):
    
        a1dat_grdc   = self.loadDailyDataArray(srcPath, dattype=dattype)
        a1dtime_grdc = self.loadDailyDTimeArray(srcPath)
    
        ndays     = (eDTimeOut-iDTimeOut).days + 1
    
        iDTimegrdc = a1dtime_grdc[0]
        eDTimegrdc = a1dtime_grdc[-1]
    
        dDTime     = timedelta(days=1)
        #------------
        if   (iDTimeOut<=iDTimegrdc)&(iDTimegrdc<=eDTimeOut):
            iout = (iDTimegrdc-iDTimeOut).days
            igrdc= 0
            if eDTimegrdc <= eDTimeOut:
                eout = (eDTimegrdc-iDTimeOut).days
                egrdc= len(a1dat_grdc)-1
            else:
                eout = ndays -1
                egrdc= (eDTimeOut-iDTimegrdc).days
    
        elif (iDTimegrdc <iDTimeOut):
            if (eDTimeOut<=eDTimegrdc):
                igrdc= (iDTimeOut-iDTimegrdc).days
                egrdc= (eDTimeOut-iDTimegrdc).days
                iout = 0
                eout = ndays-1
            elif (iDTimeOut<=eDTimegrdc)&(eDTimegrdc<eDTimeOut):
                igrdc= (iDTimeOut-iDTimegrdc).days
                egrdc= len(a1dat_grdc)-1
                iout = 0
                eout = (eDTimegrdc-iDTimeOut).days
            else:
                igrdc=0
                egrdc=-1
                iout =0
                eout =-1
        else:
                igrdc=0
                egrdc=-1
                iout =0
                eout =-1
    
    
        a1dis = ones(ndays, float32)*(-999.0)
        a1dis[iout:eout+1] = a1dat_grdc[igrdc:egrdc+1]
        #a1dtime= util.ret_lDTime(iDTimeOut, eDTimeOut, dDTime)
        return a1dis


    def loadDailyDTimeArray(self,srcPath):
        f=open(srcPath,'r');lines=f.readlines();f.close()
        
        #-- Find first line number for data --
        for i,line in enumerate(lines):
            if line[:7]=='YYYY-MM':
                ifirst=i+1
                break
        
        #-- Read data --
        ldat = deque([])
        for line in lines[ifirst:]:
            Year,Mon,Day = map(int, line.split(';')[0].split('-'))
            ldat.append( datetime(Year,Mon,Day) ) 

        return array(ldat)


    def loadDailyDataArray(self, srcPath, dattype='calc'): 
        f=open(srcPath,'r');lines=f.readlines();f.close()
        
        #-- Find first line number for data --
        for i,line in enumerate(lines):
            if line[:7]=='YYYY-MM':
                ifirst=i+1
                break
        
        #-- Read data --
        if dattype == 'org':
            icol=2
        elif dattype=='calc':
            icol=3
        else:
            print 'check dattype',dattype
            sys.exit()
        
        ldat = deque([])
        for line in lines[ifirst:]:
            ldat.append(float(line.split(';')[icol]))
        
        return array(ldat).astype(float32)
  
    
    def ret_pathMonthly(self, ID):
      rootDir = "/tank/utsumi/out/GRDC/Monthly"
      srcDir  = rootDir
      srcPath = srcDir + "/%s.csv"%(ID)
      return rootDir, srcDir, srcPath
    
    def loadMonthly(self, ID, iYM=False, eYM=False):
      srcPath = self.ret_pathMonthly(ID)[2]
      f=open(srcPath, "r")
      lines = f.readlines()
      f.close()
    
      lYM   = deque([])
      ldat  = deque([])
      for sline in lines:
        line = sline.strip().split(",")
        Year = int(line[0])
        Mon  = int(line[1])
        dat  = float(line[2])
    
        DTime = datetime(Year,Mon,1,0)
        lYM.append([Year,Mon])
        ldat.append(dat)
    
      lYM = array(lYM)
      ldat= array(ldat)
    
      #-- record period --
      if type(iYM)==bool:
        lYMout  = lYM
        ldatout = ldat
    
      else:
        iDTimeOut = datetime(iYM[0], iYM[1],1,0)
        eDTimeOut = datetime(eYM[0], eYM[1],1,0) 
        iDTimeDat = datetime(lYM[0][0],lYM[0][1],1,0)
        eDTimeDat = datetime(lYM[-1][0],lYM[-1][1],1,0)
    
        iYMDat = [lYM[0][0], lYM[0][1]]
        eYMDat = [lYM[-1][0],lYM[-1][1]]
        iYMOut = iYM
        eYMOut = eYM
    
        lYMout = util.ret_lYM(iYM, eYM)
        ldatout= ones(len(lYMout))*self.miss_out
        if eDTimeDat < iDTimeOut:
          #print "case1"
          pass
        elif ((iDTimeDat<=iDTimeOut)\
                        &(iDTimeOut<=eDTimeDat)\
                                   &(eDTimeDat<=eDTimeOut)):
          #print "case2"
          ldatout[:len(util.ret_lYM(iYMOut,eYMDat))] = ldat[-len(util.ret_lYM(iYMOut,eYMDat)):]
    
        elif ((iDTimeOut<=iDTimeDat)&(eDTimeDat<=eDTimeOut)):
          #print "case3"
          ldatout[len(util.ret_lYM(iYMOut,iYMDat))-1:len(util.ret_lYM(iYMOut,iYMDat))-1 + len(ldat)] = ldat
    
        elif ((iDTimeOut<=iDTimeDat)\
                        &(iDTimeDat<=eDTimeOut)\
                                   &(eDTimeOut<=eDTimeDat)):
          #print "case4"
          ldatout[-len(util.ret_lYM(iYMDat,eYMOut)):] = ldat[:len(util.ret_lYM(iYMDat,eYMOut))]
    
        elif eDTimeOut < iDTimeDat:
          #print "case5"
          pass
    
        elif ((iDTimeDat<=iDTimeOut)&(eDTimeOut<=eDTimeDat)):
          #print "case6"
          ldatout = ldat[len(util.ret_lYM(iYMDat,iYMOut))-1:len(util.ret_lYM(iYMDat,iYMOut))-1 + len(lYMout)]
        else:
          print "Check!! in loadMonthly"
          sys.exit()
      #----------------
    
      return lYMout, ldatout
     
    def loadMyList(self,crd="np",res="one"):
      self.srcDir     = "/tank/utsumi/data/TLSM/GRDC_Station"
      self.mylistPath = self.srcDir + "/Stations.%s.%s.csv"%(crd,res)
      self.crd        = crd
      self.res        = res
    
      #-- load GRDC Station list ---------
      mylistPath = self.mylistPath
      f = open(mylistPath, "r")
      lines = f.readlines()
      f.close()
      lstnID   = []
      drivnum  = {}
      dyx      = {}
      dArea    = {}  # model
      drivName = {}
      dstnName = {}
      
      for sline in lines[1:]:
        line  = sline.strip().split(",")
        stnID = int(line[5])
        lstnID.append(stnID)
    
        drivnum[stnID]  = int(line[0])
        dyx[stnID]      = [int(line[1]), int(line[2])]
        dArea[stnID]    = float(line[3])
        drivName[stnID] = line[6]
        dstnName[stnID] = line[7]
    
      self.lstnID   = lstnID    
      self.drivnum  = drivnum
      self.dyx      = dyx 
      self.dArea    = dArea
      self.drivName = drivName
      self.dstnName = dstnName
      return self

