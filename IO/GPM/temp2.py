from numpy import *
import subprocess
import gzip
import StringIO

srcDir = "/work/a01/utsumi/data/GPM/TRMM.PR/L2A25/07/2010/05"
srcPath= srcDir + "/T1PR2010053071431_2A25F0007.01.gz"

fmem  = StringIO.StringIO()

f=gzip.open(srcPath,"rb")
fmem.write(f)
f.close

cmd = ["hdp", "dumpsds", "-h","%s"%(fmem)]
subprocess.call(cmd)
