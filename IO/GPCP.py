#***********************************
# Originally by Hyungjun Kim
# modified by Nobuyuki Utsumi
#***********************************
import os,sys,socket
import calendar
#from cf.io  import *
#from cf.util import *
#from numpy import arange,concatenate,zeros,ma,fromfile
from numpy import *
from datetime import datetime,timedelta
#from cf import regrid
#from cf import settings


#def yearlyGPCP(prj,year,month_dummy):
#    baseDir = os.path.join(settings.GPCP_DIR,prj)
#
#    missing     = -99999.
#    new_missing = -999.
#
#    if prj  in ['v2','v2.1','v2.2']:
#        res     = 2.5
#        fname1  = 'gpcp_%s_psg.%i' %(prj,year)
#        fname2  = 'gpcp_%s_esg.%i' %(prj,year)
#
#        aPrcp   = loadbin(os.path.join(baseDir,fname1))[144:].reshape(-1,72,144)
#        aErr    = loadbin(os.path.join(baseDir,fname2))[144:].reshape(-1,72,144)
#
#        aRe     = concatenate(zip(aPrcp,aErr))
#
#    elif prj in ['1dd','1dd_v1.1','1dd_v1.2']:
##    elif prj== '1dd':
#        res     = 1.0
#        fname   = 'gpcp_%s_p1d.%s'
#
#        aRe     = []
#        for month in range(1,13):
#            srcPath = os.path.join(baseDir,fname%(prj,'%i%02d'%(year,month)))
#
#            if os.path.exists(srcPath):
#                data    = loadbin(srcPath)[360:].reshape(-1,180,360)
#
#            else:
#                nDays   = num_days('%i%02d'%(year,month))
#                data    = zeros((nDays,180,360),'float32')+new_missing
#
#            aRe.append(data)
#
#        aRe     = concatenate(aRe)
#
#    return ma.masked_equal(aRe,missing).filled(new_missing)[:,::-1,:]

class settings(object):
  def __init__(self, prj="1dd_v1.2"):
    hostname = socket.gethostname()
    if hostname == "mizu":
      self.baseDir  = "/data1/hjkim/GPCP/%s"%(prj)

class parameters(object):
  def __init__(self, prj="1dd_v1.2"):
    if prj=="1dd_v1.2":
      self.Lat = arange(-89.5,89.5+0.01,1.0)
      self.Lon = arange(0.5,359.5+0.01,1.0)


def monthly_1dd(prj,year,month):
    sett     = settings(prj)
    #baseDir = os.path.join(settings.GPCP_DIR,prj)
    baseDir  = sett.baseDir
    print baseDir

    missing     = -99999.
    new_missing = -9999.

    res     = 1.0
    fname   = 'gpcp_%s_p1d.%s'

    srcPath = os.path.join(baseDir,fname%(prj,'%i%02d'%(year,month)))

    if os.path.exists(srcPath):
        #data    = loadbin(srcPath)[360:].reshape(-1,180,360)
        data    = fromfile(srcPath,float32)[360:].reshape(-1,180,360).byteswap()
        return (ma.masked_equal(data,missing)/(24.*60.*60.)).filled(new_missing)[:,::-1,:]   #  swap N&S, mm/day --> mm/sec

    else:
        #nDays   = num_days('%i%02d'%(year,month))
        nDays   = calendar.monthrange(year,month)[1]
        data    = zeros((nDays,180,360),'float32')+new_missing
        return data


class GPCP(object):
    '''
    prjNAME = [
                'v2',
                '1dd'
                ]

    >>> gpcp = GPCP('mon')
    >>> gpcp.full_period
    [1979,....,2008]

    >>> gpcc(1979,1989)
    ...

    '''
    prjNAME = [
                '1dd',
                'v2'
                ]

    #def __init__(self,prj,BBox=None,interpolation=False):
    def __init__(self,prj):
        self.prj    = prj
        #self.baseDir = os.path.join(settings.GPCP_DIR,prj)
        sett     = settings(prj)
        para     = parameters(prj)

        self.baseDir  = sett.baseDir
        #self.unit       = 'mm/day'
        self.unit       = 'mm/sec'
        self.missing    = -9999.
        self.Lat        = para.Lat
        self.Lon        = para.Lon
        
        FNAME   = os.listdir(self.baseDir)

        if prj in ['v2','v2.1','v2.2']:
            res     = 2.5
            YEAR    = list(set([int(s.split('.')[-1]) for s in FNAME]))
            YEAR.sort()

            self.TIME   = array([datetime(y,1,1) for y in YEAR])
#            self.TIME   = array([datetime(y,m,1) for y in YEAR
#                                                for m in range(1,13)])

            self.readFunc   = yearlyGPCP


        elif prj in ['1dd','1dd_v1.1','1dd_v1.2']:
            res     = 1.0
            YYYYMM  = [s.split('.')[-1] for s in FNAME]
            YEAR    = list(set([int(s[:4]) for s in YYYYMM]))
            YEAR.sort()

            sDT     = datetime(YEAR[0],1,1)
            eDT     = datetime(YEAR[-1],12,31)
            nDays   = (eDT-sDT).days

            self.TIME       = array([sDT+timedelta(days=1)*i for i in range(nDays)])
            self.readFunc   = monthly_1dd

        else:
            raise ValueError, '%s is not an available project'%prj

        self.full_period    = array(YEAR)
        self.dim         = [self.TIME,self.Lat,self.Lon]


    def __call__(self,sDTime,eDTime):
        '''
        sDTime : in type(int or datetime)
        eDTime : in type(int or datetime)
        '''


        if type(sDTime) == int:
            sDTime  = datetime(sDTime,1,1)

        if type(eDTime) == int:
            eDTime  = datetime(eDTime,12,31)

#        print sDTime, eDTime

        sYear   = sDTime.year
        eYear   = eDTime.year

        YEAR    = range(sYear,eYear+1)

        if self.prj     in ['v2','v2.1','v2.2']:
            self.TIME   = array([datetime(y,1,1) for y in YEAR])
#            self.TIME   = array([datetime(y,m,1) for y in YEAR
#                                                for m in range(1,13)])

            DTIME       = self.TIME


        elif self.prj   in ['1dd','1dd_v1.2']:
#            nDays   = (eDTime-sDTime).days
            nDays   = (eDTime-sDTime).days + 1  # include dDTime

            self.TIME   = array([sDTime+timedelta(days=1)*i for i in range(nDays)])

            DTIME       = [ dtime for dtime in self.TIME if dtime.day == 1 ]


        #LLy,LLx     = self.oriGrid.LLy, self.oriGrid.LLx
        #URy,URx     = self.oriGrid.URy, self.oriGrid.URx

#        print LLy,LLx, URy,URx

#        print DTIME
#        data   = concatenate(
#                            [self.readFunc(self.prj,
#                                           dtime.year,
#                                           dtime.month)[:,LLy:URy+1,LLx:URx+1] for dtime in DTIME]
#                                )

        data   = concatenate(
                            [self.readFunc(self.prj,
                                           dtime.year,
                                           dtime.month) for dtime in DTIME]
                                )


#        if self.oriGrid.res != self.grid.res:
#            data    = array([regrid(self.oriGrid.LAT,self.oriGrid.LON,dat,
#                                          self.grid.LAT,self.grid.LON)
#                                        for dat in data])

        sN          = sDTime.day-1
        eN          = sN + nDays-1
        self.Data   = data[sN:eN+1]
        self.dim    = [self.TIME,self.Lat,self.Lon]

