#! /usr/bin/python
#--------------------------------------------------------------
# CREATED BY : N.Utsumi
# BASED ON   : GPyM module by hjkim
#--------------------------------------------------------------
import os,sys

class CloudSat_data(object):
    def __init__(self):
        self.srcPath    = []
        self.recLen     = []
        self.lat        = []
        self.lon        = []
        self.dtime      = []
        self.tbound     = []
        self.data       = []
        self.griddata   = []
        self.grid       = []
