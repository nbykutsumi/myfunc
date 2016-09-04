from   numpy import *
import struct

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


class CloudWNP(object):
  def __init__(self):
    """   
    Cloud Type Table
    0    : Clear Sky
    1    : Cb   (Cumulonimbus)
    201  : High Clouds
    202  : Mid Clouds
    4    : Cu   (Cumulus)
    3    : Sc   (Stratocumulus)
    204  : Fog/Stratus
    200  : Cloudy Sky 
    """   
 
    #DType = "tac"  # Total Cloud Amount
    #DType = "ahc"  # Upper Cloud Amount
    #DType = "cvc"  # Convective Cloud Amount
    #DType = "clc"  # Cloud Type
    #DType = "htc"  # Cloud Top Height
    
    self.dD    = {"tac":0
                 ,"ahc":0
                 ,"cvc":0
                 ,"clc":0
                 ,"htc":-2}
    
    self.ny    = 261
    self.nx    = 265
    self.BBox  = [[-0.1, 113.875],[52.1, 180.125]]  # Boundary, not center of grid box
    self.dLat  = 0.20
    self.dLon  = 0.25
    self.Lat   = arange(0.0, 52.0+0.01, 0.2)
    self.Lon   = arange(114.0, 180.0+0.01, 0.25)
    self.baseDir = "/tank/utsumi/CLOUDTYPE/WNPAC"

    self.dclName ={0:"Clear Sky",   1:"Cumulonimbus(Cb)"
         ,2:"High Cloud" , 3:"Mid Cloud"
         ,4:"Cumulus(Cu)", 5:"Stratocumulus(Sc)"
         ,6:"Fog/St"     , 7:"Cloudy", 99:"All"}

    self.dclShortName={0:"no", 1:"Cb",  2:"hi",3:"md"
             ,4:"Cu", 5:"Sc",  6:"St",7:"cw", 99:"All"}

    self.licl    = range(0,7+1)
    self.dclid   = {0:0, 1:1, 2:201, 3:202, 4:4, 5:3, 6:204, 7:200}
  
  def decode_grib2_data(self, string, R, E, D):
  
      aSrc    = fromstring( string, 'uint8' )
  
      aOut    = (R + aSrc * 2**E)/10**D
      return array( aOut ).reshape(self.ny, self.nx)

  
  
  def decode_grib2_section(self, fmt, string):
      lenFmt  = struct.calcsize(fmt)
  
      if lenFmt != len(string):
          fmt     = fmt + '%is'%(len(string)-lenFmt)
  
      return struct.unpack(fmt, string)
  

  def loadData(self,  DTime, DType="clc"):
    """
    #DType = "tac"  # Total Cloud Amount
    #DType = "ahc"  # Upper Cloud Amount
    #DType = "cvc"  # Convective Cloud Amount
    #DType = "clc"  # Cloud Type
    #DType = "htc"  # Cloud Top Height
    """

    Year    = DTime.year
    Mon     = DTime.month
    Day     = DTime.day
    Hour    = DTime.hour  # Instantaneous, UTC 
    self.srcDir  = self.baseDir + "/%04d%02d/%04d%02d%02d"%(Year,Mon,Year,Mon,Day)
    self.srcPath = self.srcDir + "/Z__C_RJTD_%04d%02d%02d%02d0000_OBS_SAT_PS%s_RDnwp_grib2.bin"%(Year,Mon,Day,Hour,DType)
    
    byteorder  = ">"
    Fmt     = [ '4s2sssQ',                          # section 0  # temp
                'ishhssshbbbbbss',                  # section 1  # temp
                '',                                 # section 2  # temp
                'ississHssisis7is4is',              # section 3  # temp
                'ibHH3bssH2bibsissi',               # section 4  
                'ibihfhhbb',                        # section 5  # temp
                'iss',                              # section 6
                'is',                               # section 7
                '4s'                                # section 8
               ]
    Fmt     = [byteorder+fmt if fmt != '' else '' for fmt in Fmt]

    try:
      srcFile = open( self.srcPath )
    except IOError:
      print self.srcPath
      raise IOError 
    
    Section = []
    
    Section.append( struct.unpack(Fmt[0], srcFile.read( struct.calcsize(Fmt[0]) )) )
    
    for fmt in Fmt[1:-1]:
    
        if fmt == '':
            Section.append( () )
            continue
    
        first4byte  = srcFile.read(4)
        length  = struct.unpack(fmt[:2], first4byte)[0]
        string  = first4byte + srcFile.read(length-4)
        Section.append( self.decode_grib2_section( fmt, string ) )
    
    # test
    #print Section[1]

    Section.append( struct.unpack(Fmt[-1], srcFile.read( struct.calcsize(Fmt[-1]) )) )
    
    R   = 0.0
    E   = 0
    D   = self.dD[DType]  
    return flipud(self.decode_grib2_data( Section[7][-1], R,E,D))

  def loadNumMon(self, Year,Mon,cltype):
    """
    self.dclName ={0:"Clear Sky",   1:"Cumulonimbus(Cb)"
         ,2:"High Cloud" , 3:"Mid Cloud"
         ,4:"Cumulus(Cu)", 5:"Stratocumulus(Sc)"
         ,6:"Fog/St"     , 7:"Cloudy", 99:"All"}

    self.dclShortName={0:"no", 1:"Cb",  2:"hi",3:"md"
             ,4:"Cu", 5:"Sc",  6:"St",7:"cw", 99:"All"}

    cltype = "no", "Cb", "hi", "md", "Cu", "Sc", "St", "cw", "All"
      or
    cltype = 1 - 7 & 99
    """
    if type(cltype)==int:
      cltype = self.dclShortName[cltype]
    sDir  = self.baseDir + "/num"
    sPath = sDir + "/num.201408.Sc.261x265"
    sPath = sDir + "/num.%04d%02d.%s.%dx%d"%(Year,Mon,cltype,self.ny,self.nx)
    return fromfile(sPath, int32).reshape(self.ny, self.nx)

  def loadNumAcc(self, iYM, eYM, cltype):
    """
    self.dclName ={0:"Clear Sky",   1:"Cumulonimbus(Cb)"
         ,2:"High Cloud" , 3:"Mid Cloud"
         ,4:"Cumulus(Cu)", 5:"Stratocumulus(Sc)"
         ,6:"Fog/St"     , 7:"Cloudy", 99:"All"}

    self.dclShortName={0:"no", 1:"Cb",  2:"hi",3:"md"
             ,4:"Cu", 5:"Sc",  6:"St",7:"cw", 99:"All"}

    cltype = "no", "Cb", "hi", "md", "Cu", "Sc", "St", "cw", "All"
      or
    cltype = 1 - 7 & 99
    """
    lYM    = ret_lYM(iYM, eYM)
 
    return array([self.loadNumMon(Year,Mon,cltype)
                 for [Year,Mon] in lYM]).sum(axis=0)


class MyCloudWNP(CloudWNP):
  def __init__(self, ver=1):
    CloudWNP.__init__(self)
    self.baseDir = "/home/utsumi/mnt/well.share/CLOUDTYPE/MyWNP%d"%(ver)

    if   ver == 1:
      self.dclName ={0:"Clear Sky",   1:"Deep Convection"
           ,2:"High Clouds"
           ,3:"Mid & Low Clouds", 4:"Mixed Clouds", 99:"All"}
  
      self.dclShortName={0:"no", 1:"dc", 2:"hi"
               ,3:"ml", 4:"mx", 99:"All"}

    elif ver == 2:
      self.dclName ={0:"Clear Sky"
           ,1:"Deep Convection I"
           ,2:"Deep Convection II"
           ,3:"High Clouds"
           ,4:"Mid & Low Clouds"
           ,5:"Mixed Clouds"
           ,99:"All"}
  
      self.dclShortName={0:"no", 1:"c1",2:"c2", 3:"hi"
               ,4:"ml", 5:"mx", 99:"All"}

    self.ncl     = len(self.dclName.keys())-1  
    self.licl    = range(self.ncl)
    #self.dclid   = {0:0, 1:1, 2:2, 3:3, 4:4}
    self.dclid   = {i:i for i in self.licl}
 

  def loadData(self, DTime):
    Year    = DTime.year
    Mon     = DTime.month
    Day     = DTime.day
    Hour    = DTime.hour
    srcDir  = self.baseDir + "/%04d%02d/%02d"%(Year,Mon,Day)
    srcPath = srcDir + "/CLTYPE.%04d%02d%02d%02d.%dx%d"%(Year,Mon,Day,Hour,self.ny,self.nx)
    return fromfile(srcPath, int32).reshape(self.ny, self.nx)




