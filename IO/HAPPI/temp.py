from datetime import datetime, timedelta
import myfunc.IO.HAPPI as HAPPI

hp = HAPPI.Happi()

prj  = "C20"
#var  = "T850"
var  = "u500"
expr = "ALL"
ens  = 1

hp(prj,expr,ens)
DTime = datetime(2006,2,20,0)
#a     = hp.load_6hr(var, DTime, verbose=True)
a     = hp.load_day(var, DTime)
print a
