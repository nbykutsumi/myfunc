C     -*- fortran -*-
C     This file is autogenerated with f2py (version:2)
C     It contains Fortran 77 wrappers to fortran functions.

      subroutine f2pywraprgetara (rgetaraf2pywrap, rlon1, rlon2, r
     &lat1, rlat2)
      external rgetara
      real*8 rlon1
      real*8 rlon2
      real*8 rlat1
      real*8 rlat2
      double precision rgetaraf2pywrap, rgetara
      rgetaraf2pywrap = rgetara(rlon1, rlon2, rlat1, rlat2)
      end

