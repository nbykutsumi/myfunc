#! /usr/bin/python
#--------------------------------------------------------------
# CREATED BY : N.Utsumi
# BASED ON   : GPyM module by hjkim
#--------------------------------------------------------------
import  os,sys
from    numpy      import asarray
from    pyhdf      import HDF, VS
from    itertools  import chain


def read_hdf4_vs(srcPath, varName, Slice=None, verbose=True):

    if Slice == None:   Slice = slice(None,None,None)

    try:
        f = HDF.HDF(srcPath)
        vs = f.vstart()
        instVar = vs.attach(varName)
        lOut    = instVar[:][Slice]
        instVar.detach()
        vs.end()
        f.close()
        
        aOut = asarray(list(chain.from_iterable(lOut)))
    except:
        print '!'*80
        print 'I/O Error'
        print 'Blank File? %s'%srcPath
        print 'Blank array will be returned [ %s ]'%varName
        print Slice
        print '!'*80


    if verbose  == True:
        print '\t[READ_HDF4] %s [%s] -> %s'%( srcPath, varName, aOut.shape)

    return aOut


def main(args,opts):
    print args
    print opts

    return

if __name__=='__main__':
    usage   = 'usage: %prog [options] arg'
    version = '%prog 1.0'

    main(args,options)
