from   numpy import *
import struct

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
    
  
  
