module upscale_fsub

contains
!!******************************************************************
SUBROUTINE divide_a2array(a2in, ndiv_x, ndiv_y, nx, ny, a2out)
implicit none
!
integer                                  nx, ny
!---- in ----------
real,dimension(nx,ny)                 :: a2in
!f2py intent(in)                         a2in
integer                                  ndiv_x, ndiv_y
!f2py intent(in)                         ndiv_x, ndiv_y
!---- out ---------
real,dimension(nx*ndiv_x, ny*ndiv_y)  :: a2out
!f2py intent(out)                        a2out
!---- calc --------
integer                                  ix_in, iy_in
!------------------
do iy_in = 1, ny
  do ix_in = 1, nx
    a2out((ix_in-1)*ndiv_x+1: ix_in*ndiv_x, (iy_in-1)*ndiv_y+1: iy_in*ndiv_y) = a2in(ix_in, iy_in)
  end do
end do 

return 
END SUBROUTINE divide_a2array
!!******************************************************************
SUBROUTINE mk_3x3sum_one(a2in, miss, nx, ny, a2out)
implicit none
!
integer                                  nx, ny
!--- in ----------
real,dimension(nx,ny)                 :: a2in
!f2py intent(in)                         a2in
real                                     miss
!f2py intent(in)                         miss
!--- out --------
real,dimension(nx,ny)                 :: a2out
!f2py intent(out)                        a2out
!--- calc -------
real                                     v
integer                                  ix, iy, iix, iiy, dx, dy, nmiss
!----------------
do iy = 1,ny,3
  do ix = 1,nx,3
    !-------------
    v     = 0.0
    nmiss = 0
    do dy = 0,2
      iiy = iy + dy
      do dx = 0,2
        iix = ix + dx
        if (a2in(iix,iiy).eq.miss)then
          nmiss = nmiss + 1
        else
          v     = v + a2in(iix,iiy)
        end if
      end do
    end do
    !-------------
    if (nmiss.eq.9)then
      a2out(ix:ix+2, iy:iy+2) = miss
    else
      a2out(ix:ix+2, iy:iy+2) = v
    end if
  end do
end do

!----------------
return
END SUBROUTINE mk_3x3sum_one
!******************************************************************
SUBROUTINE mk_a2convolution(a2in, a2filter, miss, nrad, nx, ny, a2out)
implicit none
!-- dims ---------
integer                                  nx, ny
integer                                  nrad
!-- in -----------
real,dimension(nx,ny)                 :: a2in
!f2py intent(in)                         a2in
real,dimension(2*nrad+1,2*nrad+1)     :: a2filter
!f2py intent(in)                         a2filter            
real                                     miss
!f2py intent(in)                         miss
!-- out ----------
!real,dimension(nx+4,ny+4)             :: a2out
real,dimension(nx,ny)                 :: a2out
!f2py intent(out)                        a2out
!-- calc ---------
integer                                  ix, iy, iix, iiy, dx,dy, nnx, nny
real,dimension(nx+2*nrad,ny+2*nrad)       :: a2large_in, a2large_out
real                                     vsum, wgtsum
!-----------------

!---!-------!---!
! A !   B   ! C ! 
!---!-------!---!
!   !       !   !
! D !   E   ! F !
!   !       !   !
!---!-------!---!
! G !   H   ! I !
!---!-------!---!

nnx   = nx + 2*nrad
nny   = ny + 2*nrad
!a2large_in = 1.0
!-----------------
!-A-!
a2large_in(1:nrad,1:nrad) = miss
!-B-!
a2large_in(nrad+1:nx+nrad, 1:nrad) = miss
!-C-!
a2large_in(nx+nrad+1: nnx, 1:nrad) = miss
!-D-!
a2large_in(1:nrad, nrad+1:ny+nrad) = a2in(nx-nrad+1:nx, 1:ny)
!-E-!
a2large_in(nrad+1:nx+nrad, nrad+1:ny+nrad) = a2in(:,:)
!-F-!
a2large_in(nx+nrad+1:nnx, nrad+1:ny+nrad) = a2in(1:nrad, 1:ny)
!-G-!
a2large_in(1:nrad,ny+nrad+1:nny) = miss
!-H-!
a2large_in(nrad+1:nx+nrad, ny+nrad+1:nny) = miss
!-I-!
a2large_in(nx+nrad+1:nnx, ny+nrad+1:nny)  = miss
!
a2large_out = a2large_in

do ix = 1+nrad, nnx-nrad
  do iy = 1+nrad, nny-nrad
    if (a2large_in(ix,iy).eq.miss)then
      continue
    else
      vsum   = 0.0
      wgtsum = 0.0 
      do dy = -nrad, nrad
        iiy = iy + dy
        do dx = -nrad, nrad
          iix = ix + dx
          if (a2large_in(iix,iiy).ne.miss)then
            vsum   = vsum + a2large_in(iix,iiy) * a2filter(nrad+dx+1,nrad+dy+1)
            wgtsum = wgtsum + a2filter(nrad+dx+1,nrad+dy+1)
            !-----------
          end if
        end do
      end do
      a2large_out(ix,iy) = vsum / wgtsum
    end if
  end do
end do
a2out = a2large_out(nrad+1:nx+nrad, nrad+1:ny+nrad)
!a2out = a2large_out
!
!a2out = -9999.0
!-----------------
return
END SUBROUTINE mk_a2convolution
!******************************************************************

!******************************************************************
SUBROUTINE mk_a2convolution_3x3(a2in, a2filter, miss, nx, ny, a2out)
implicit none
!-- dims ---------
integer                                  nx, ny
!-- in -----------
real,dimension(nx,ny)                 :: a2in
!f2py intent(in)                         a2in
real,dimension(3,3)                   :: a2filter
!f2py intent(in)                         a2filter            
real                                     miss
!f2py intent(in)                         miss
!-- out ----------
!real,dimension(nx+4,ny+4)             :: a2out
real,dimension(nx,ny)                 :: a2out
!f2py intent(out)                        a2out
!-- calc ---------
integer                                  ix, iy, iix, iiy, dx,dy, nnx, nny
real,dimension(nx+2,ny+2)             :: a2large_in, a2large_out
real                                     vsum, wgtsum
!-----------------

!---!-------!---!
! A !   B   ! C ! 
!---!-------!---!
!   !       !   !
! D !   E   ! F !
!   !       !   !
!---!-------!---!
! G !   H   ! I !
!---!-------!---!

nnx   = nx + 2
nny   = ny + 2
!a2large_in = 1.0
!-----------------
!-A-!
a2large_in(1,1) = miss
!-B-!
a2large_in(2:nnx-1,1) = miss
!-C-!
a2large_in(nnx,1) = miss
!-D-!
a2large_in(1, 2:nny-1) = a2in(nx, 1:ny)
!-E-!
a2large_in(2:nnx-1,2:nny-1) = a2in(:,:)
!-F-!
a2large_in(nnx,2:nny-1) = a2in(1, 1:ny)
!-G-!
a2large_in(1,nny) = miss
!-H-!
a2large_in(2:nnx-1, nny) = miss
!-I-!
a2large_in(nnx, nny) = miss
!
a2large_out = a2large_in
do ix = 2, nnx-1
  do iy = 2, nny-1
    if (a2large_in(ix,iy).eq.miss)then
      continue
    else
      vsum   = 0.0
      wgtsum = 0.0 
      do dy = -1, 1
        iiy = iy + dy
        do dx = -1, 1
          iix = ix + dx
          if (a2large_in(iix,iiy).ne.miss)then
            vsum   = vsum + a2large_in(iix,iiy) * a2filter(dx+2,dy+2)
            wgtsum = wgtsum + a2filter(dx+2,dy+2)
            !-----------
          end if
        end do
      end do
      a2large_out(ix,iy) = vsum / wgtsum
    end if
  end do
end do
a2out = a2large_out(2:nnx-1, 2:nny-1)
!a2out = a2large_out

!a2out = a2in
!-----------------
return
END SUBROUTINE mk_a2convolution_3x3
!******************************************************************


!******************************************************************
SUBROUTINE mk_a2convolution_5x5(a2in, a2filter, miss, nx, ny, a2out)
implicit none
!-- dims ---------
integer                                  nx, ny
!-- in -----------
real,dimension(nx,ny)                 :: a2in
!f2py intent(in)                         a2in
real,dimension(5,5)                   :: a2filter
!f2py intent(in)                         a2filter            
real                                     miss
!f2py intent(in)                         miss
!-- out ----------
!real,dimension(nx+4,ny+4)             :: a2out
real,dimension(nx,ny)                 :: a2out
!f2py intent(out)                        a2out
!-- calc ---------
integer                                  ix, iy, iix, iiy, dx,dy, nnx, nny
real,dimension(nx+4,ny+4)             :: a2large_in, a2large_out
real                                     vsum, wgtsum
!-----------------

!---!-------!---!
! A !   B   ! C ! 
!---!-------!---!
!   !       !   !
! D !   E   ! F !
!   !       !   !
!---!-------!---!
! G !   H   ! I !
!---!-------!---!

nnx   = nx + 4
nny   = ny + 4
!a2large_in = 1.0
!-----------------
!-A-!
a2large_in(1:2,1:2) = miss
!-B-!
a2large_in(3:nnx-2,1:2) = miss
!-C-!
a2large_in(nnx-1:nnx,1:2) = miss
!-D-!
a2large_in(1:2, 3:nny-2) = a2in(nx-1:nx, 1:ny)
!-E-!
a2large_in(3:nnx-2,3:nny-2) = a2in(:,:)
!-F-!
a2large_in(nnx-1:nnx,3:nny-2) = a2in(1:2, 1:ny)
!-G-!
a2large_in(1:2,nny-1:nny) = miss
!-I-!
a2large_in(nnx-1:nnx, nny-1:nny) = miss
!-H-!
a2large_in(3:nnx-2,nny-1:nny) = miss
!
a2large_out = a2large_in
do ix = 3, nnx-2
  do iy = 3, nny-2
    if (a2large_in(ix,iy).eq.miss)then
      continue
    else
      vsum   = 0.0
      wgtsum = 0.0 
      do dy = -2, 2
        iiy = iy + dy
        do dx = -2, 2
          iix = ix + dx
          if (a2large_in(iix,iiy).ne.miss)then
            vsum   = vsum + a2large_in(iix,iiy) * a2filter(dx+3,dy+3)
            wgtsum = wgtsum + a2filter(dx+3,dy+3)
            !-----------
          end if
        end do
      end do
      a2large_out(ix,iy) = vsum / wgtsum
    end if
  end do
end do
a2out = a2large_out(3:nnx-2, 3:nny-2)
!a2out = a2large_out

!a2out = a2in
!-----------------
return
END SUBROUTINE mk_a2convolution_5x5
!******************************************************************
SUBROUTINE upscale(  a2fin&
                  &, a1lon_fin, a1lat_fin&
                  &, a1lon_out, a1lat_out&
                  &, pergrid, globflag, missflag, miss_in, miss_out&
                  &, nlon_fin, nlat_fin&
                  &, nlon_out, nlat_out&
                  &, a2out)
!------------------------
! pergrid = 0: per area (e.g. mm/m2), others (e.g, K, kg/kg, mm/s)
! pergrid = 1: per grid (e.g. km2/grid, population/grid) 
! 
! globflag =1: for global data ( left of the ix=1 is ix=nx)


implicit none
!-- dims -----------
integer                                  nlon_fin, nlat_fin
integer                                  nlon_out, nlat_out
!-- in -------------
real,dimension(nlon_fin, nlat_fin)    :: a2fin
!f2py intent(in)                         a2fin
real,dimension(nlon_fin)              :: a1lon_fin
real,dimension(nlat_fin)              :: a1lat_fin
!f2py intent(in)                         a1lon_fin, a1lat_fin
real,dimension(nlon_out)              :: a1lon_out
real,dimension(nlat_out)              :: a1lat_out
!f2py intent(in)                         a1lon_out, a1lat_out
integer                                  pergrid
!f2py intent(in)                         pergrid
integer                                  globflag
!f2py intent(in)                         globflag
integer                                  missflag
!f2py intent(in)                         missflag
real                                     miss_in
!f2py intent(in)                         miss_in
real                                     miss_out
!f2py intent(in)                         miss_out


!-- out ------------
real,dimension(nlon_out, nlat_out)    :: a2out
!f2py intent(out)                        a2out

!-- para -----------

!-- calc -----------
integer,dimension(nlon_fin)           :: a1xw_corres_fort, a1xe_corres_fort
integer,dimension(nlat_fin)           :: a1ys_corres_fort, a1yn_corres_fort
real,dimension(nlon_fin, nlat_fin)    :: a2areasw, a2arease, a2areanw, a2areane
real,dimension(nlon_out, nlat_out)    :: a2areaout
!-- init -----------
a2areaout = 0.0
a2out     = 0.0
!-------------------
CALL upscale_prep(a1lon_fin, a1lat_fin, a1lon_out, a1lat_out, globflag&
                           &, nlon_fin, nlat_fin, nlon_out, nlat_out&
                           &, a1xw_corres_fort, a1xe_corres_fort&
                           &, a1ys_corres_fort, a1yn_corres_fort&
                           &, a2areasw, a2arease, a2areanw, a2areane)


CALL  upscale_fast(  a2fin&
                  &, a1xw_corres_fort, a1xe_corres_fort&
                  &, a1ys_corres_fort, a1yn_corres_fort&
                  &, a2areasw, a2arease, a2areanw, a2areane&
                  &, nlon_out, nlat_out&
                  &, pergrid, missflag, miss_in, miss_out&
                  &, nlon_fin, nlat_fin&
                  &, a2out)
!-------------------
return
END SUBROUTINE upscale
!
!******************************************************************
SUBROUTINE upscale_fast(  a2fin&
                  &, a1xw_corres_fort, a1xe_corres_fort&
                  &, a1ys_corres_fort, a1yn_corres_fort&
                  &, a2areasw, a2arease, a2areanw, a2areane&
                  &, nlon_out, nlat_out&
                  &, pergrid, missflag, miss_in, miss_out&
                  &, nlon_fin, nlat_fin&
                  &, a2out)
!------------------------
! pergrid = 0: per area (e.g. mm/m2), others (e.g, K, kg/kg, mm/s)
! pergrid = 1: per grid (e.g. km2/grid, population/grid) 
! missflag= 0: nocheck for missing value
! missflag= 1: check missing value
!------------------------
implicit none
!-- in -------------
integer                                  nlon_fin, nlat_fin
integer                                  nlon_out, nlat_out
!f2py intent(in)                         nlon_out, nlat_out
integer,dimension(nlon_fin)           :: a1xw_corres_fort, a1xe_corres_fort
!f2py intent(in)                      :: a1xw_corres_fort, a1xe_corres_fort
integer,dimension(nlat_fin)           :: a1ys_corres_fort, a1yn_corres_fort
!f2py intent(in)                      :: a1ys_corres_fort, a1yn_corres_fort
real,dimension(nlon_fin, nlat_fin)    :: a2fin
!f2py intent(in)                         a2fin
real,dimension(nlon_fin, nlat_fin)    :: a2areasw, a2arease, a2areanw, a2areane
!f2py intent(in)                      :: a2areasw, a2arease, a2areanw, a2areane
integer                                  pergrid, missflag
!f2py intent(in)                         pergrid, missflag
real                                     miss_in
!f2py intent(in)                         miss_in
real                                     miss_out
!f2py intent(in)                         miss_out

!-- out ------------
real,dimension(nlon_out, nlat_out)    :: a2out
!f2py intent(out)                        a2out
!-- calc -----------
integer                                  ixfin, iyfin, ixout, iyout
real,dimension(nlon_fin, nlat_fin)    :: a2areafin
real,dimension(nlon_out, nlat_out)    :: a2areaout
real                                     areafin_seg, areafin_all
!-- parameter ------
integer,parameter                     :: miss_int = -9999
!-- init -----------
a2areaout = 0.0
a2out     = 0.0
!-------------------
a2areafin = a2areasw + a2arease + a2areanw + a2areane
!
if (pergrid .eq. 0)then
  do iyfin = 1,nlat_fin
    do ixfin = 1,nlon_fin
      !-- sw -----
      ixout = a1xw_corres_fort(ixfin)
      iyout = a1ys_corres_fort(iyfin)
      areafin_seg  = a2areasw(ixfin,iyfin)
      a2areaout(ixout,iyout)  = a2areaout(ixout,iyout) + areafin_seg
      a2out(ixout,iyout)      = a2out(ixout,iyout) + a2fin(ixfin,iyfin)*areafin_seg

      !-- se -----
      ixout = a1xe_corres_fort(ixfin)
      iyout = a1ys_corres_fort(iyfin)
      areafin_seg  = a2arease(ixfin,iyfin)
      a2areaout(ixout,iyout)  = a2areaout(ixout,iyout) + areafin_seg
      a2out(ixout,iyout)      = a2out(ixout,iyout) + a2fin(ixfin,iyfin)*areafin_seg

      !-- nw -----
      ixout = a1xw_corres_fort(ixfin)
      iyout = a1yn_corres_fort(iyfin)
      areafin_seg  = a2areanw(ixfin,iyfin)
      a2areaout(ixout,iyout)  = a2areaout(ixout,iyout) + areafin_seg
      a2out(ixout,iyout)      = a2out(ixout,iyout) + a2fin(ixfin,iyfin)*areafin_seg

      !-- ne -----
      ixout = a1xe_corres_fort(ixfin)
      iyout = a1yn_corres_fort(iyfin)
      areafin_seg  = a2areane(ixfin,iyfin)
      a2areaout(ixout,iyout)  = a2areaout(ixout,iyout) + areafin_seg
      a2out(ixout,iyout)      = a2out(ixout,iyout) + a2fin(ixfin,iyfin)*areafin_seg
    end do
  end do
  a2out  = a2out / a2areaout
else if (pergrid .eq. 1)then
  do iyfin = 1,nlat_fin
    do ixfin = 1,nlon_fin
      !-- area all ---
      areafin_all  = a2areafin(ixfin, iyfin)
      !-- sw -----
      ixout = a1xw_corres_fort(ixfin)
      iyout = a1ys_corres_fort(iyfin)
      areafin_seg  = a2areasw(ixfin,iyfin)
      a2out(ixout,iyout)      = a2out(ixout,iyout) + a2fin(ixfin,iyfin)*areafin_seg /areafin_all
      !-- se -----
      ixout = a1xe_corres_fort(ixfin)
      iyout = a1ys_corres_fort(iyfin)
      areafin_seg  = a2arease(ixfin,iyfin)
      a2out(ixout,iyout)      = a2out(ixout,iyout) + a2fin(ixfin,iyfin)*areafin_seg /areafin_all
      !-- nw -----
      ixout = a1xw_corres_fort(ixfin)
      iyout = a1yn_corres_fort(iyfin)
      areafin_seg  = a2areanw(ixfin,iyfin)
      a2out(ixout,iyout)      = a2out(ixout,iyout) + a2fin(ixfin,iyfin)*areafin_seg /areafin_all
      !-- ne -----
      ixout = a1xe_corres_fort(ixfin)
      iyout = a1yn_corres_fort(iyfin)
      areafin_seg  = a2areane(ixfin,iyfin)
      a2out(ixout,iyout)      = a2out(ixout,iyout) + a2fin(ixfin,iyfin)*areafin_seg /areafin_all

    end do
  end do
end if
!!-------------------
!! check miss
!!-------------------
if (missflag .eq.1)then
  do iyfin = 2, nlat_fin-1
    do ixfin = 2, nlon_fin-1
      if (a2fin(ixfin,iyfin) .eq. miss_in)then
        !-- sw -----
        ixout = a1xw_corres_fort(ixfin)
        iyout = a1ys_corres_fort(iyfin)
        a2out(ixout,iyout)      = miss_out
        !-- se -----
        ixout = a1xe_corres_fort(ixfin)
        iyout = a1ys_corres_fort(iyfin)
        a2out(ixout,iyout)      = miss_out
        !-- nw -----
        ixout = a1xw_corres_fort(ixfin)
        iyout = a1yn_corres_fort(iyfin)
        a2out(ixout,iyout)      = miss_out
        !-- ne -----
        ixout = a1xe_corres_fort(ixfin)
        iyout = a1yn_corres_fort(iyfin)
        a2out(ixout,iyout)      = miss_out
      end if
    end do
  end do
  !-- only northern and southern edges ---
  do iyfin = 1, nlat_fin, nlat_fin-1
    do ixfin = 1, nlon_fin
      if (a2fin(ixfin,iyfin) .eq. miss_in)then
        !-- sw -----
        ixout = a1xw_corres_fort(ixfin)
        iyout = a1ys_corres_fort(iyfin)
        if ((ixout.ne.miss_int).and.(iyout.ne.miss_int))then
          a2out(ixout,iyout)      = miss_out
        end if
        !-- se -----
        ixout = a1xe_corres_fort(ixfin)
        iyout = a1ys_corres_fort(iyfin)
        if ((ixout.ne.miss_int).and.(iyout.ne.miss_int))then
          a2out(ixout,iyout)      = miss_out
        end if
        !-- nw -----
        ixout = a1xw_corres_fort(ixfin)
        iyout = a1yn_corres_fort(iyfin)
        if ((ixout.ne.miss_int).and.(iyout.ne.miss_int))then
          a2out(ixout,iyout)      = miss_out
        end if
        !-- ne -----
        ixout = a1xe_corres_fort(ixfin)
        iyout = a1yn_corres_fort(iyfin)
        if ((ixout.ne.miss_int).and.(iyout.ne.miss_int))then
          a2out(ixout,iyout)      = miss_out
        end if
      end if
    end do
  end do
  !-- only western and eastern edges except corners ---
  do iyfin = 2, nlat_fin-1
    do ixfin = 1, nlon_fin, nlon_fin-1
      if (a2fin(ixfin,iyfin) .eq. miss_in)then
        !-- sw -----
        ixout = a1xw_corres_fort(ixfin)
        iyout = a1ys_corres_fort(iyfin)
        if ((ixout.ne.miss_int).and.(iyout.ne.miss_int))then
          a2out(ixout,iyout)      = miss_out
        end if
        !-- se -----
        ixout = a1xe_corres_fort(ixfin)
        iyout = a1ys_corres_fort(iyfin)
        if ((ixout.ne.miss_int).and.(iyout.ne.miss_int))then
          a2out(ixout,iyout)      = miss_out
        end if
        !-- nw -----
        ixout = a1xw_corres_fort(ixfin)
        iyout = a1yn_corres_fort(iyfin)
        if ((ixout.ne.miss_int).and.(iyout.ne.miss_int))then
          a2out(ixout,iyout)      = miss_out
        end if
        !-- ne -----
        ixout = a1xe_corres_fort(ixfin)
        iyout = a1yn_corres_fort(iyfin)
        if ((ixout.ne.miss_int).and.(iyout.ne.miss_int))then
          a2out(ixout,iyout)      = miss_out
        end if
      end if
    end do
  end do
end if  

return
END SUBROUTINE upscale_fast
!******************************************************************
SUBROUTINE mk_a2area_sphere(a1lon, a1lat, nlon, nlat, a2area)
implicit none
!--- in ----------
integer                                 nlon, nlat

real,dimension(nlon)                 :: a1lon
!f2py intent(in)                        a1lon
real,dimension(nlat)                 :: a1lat
!f2py intent(in)                        a1lat
!--- out ---------
real,dimension(nlon, nlat)           :: a2area
!f2py intent(out)                       a2area
!--- para --------
real,parameter                       :: r = 6371.012  ! (km)
real,parameter                       :: pi = 3.1416
!--- calc --------
integer                                 ix, iy
real,dimension(nlon)                 :: a1lonw, a1lone
real,dimension(nlat)                 :: a1lats, a1latn
real                                    lats, latn, lonw, lone
!-----------------
a2area  = -9999.0
!
!--- lon w and e ------
do ix = 2,nlon -1
  a1lonw(ix)   = (a1lon(ix) + a1lon(ix-1))*0.5
  a1lone(ix)   = (a1lon(ix+1) + a1lon(ix))*0.5
end do
a1lonw(1)        = (a1lon(nlon)-360.0 + a1lon(1))*0.5
a1lone(1)        = (a1lon(1) + a1lon(2))*0.5
a1lonw(nlon) = (a1lon(nlon) + a1lon(nlon-1))*0.5
a1lone(nlon) = (a1lon(nlon) + a1lon(1)+360.0)*0.5
!--- lat s and n ------
do iy = 2,nlat -1
  a1lats(iy)   = (a1lat(iy) + a1lat(iy-1))*0.5
  a1latn(iy)   = (a1lat(iy+1) + a1lat(iy))*0.5
end do
a1lats(1)        = -90.0
a1latn(1)        = (a1lat(1) + a1lat(2))*0.5
a1lats(nlat) = (a1lat(nlat) + a1lat(nlat-1))*0.5
a1latn(nlat) = 90.0
!----------------------
do iy = 1, nlat
  lats = a1lats(iy)
  latn = a1latn(iy)
  do ix = 1, nlon
    lonw  = a1lonw(ix)
    lone  = a1lone(ix)
    a2area(ix,iy) = cal_area_sphere(lats, latn, lonw, lone)
  end do
end do

!----------------------
return
END SUBROUTINE mk_a2area_sphere



!******************************************************************
FUNCTION cal_area_sphere(lats, latn, lonw, lone)
!----------------------
! estimate area (km2) assuming that the eath is a sphere
! S = r2 * dlon * pi / 180 * (sin(lat2) - sin(lat1))
! lat, lon are in degree
!----------------------
implicit none
!--- in -----------
real                                    lats, latn, lonw, lone  ! (deg.)
!f2py intent(in)                        lats, latn, lonw, lone

!--- out ----------
real                                    cal_area_sphere
!f2py intent(out)                       cal_area_sphere
!--- para ---------
real,parameter                       :: r = 6371.012  ! (km)
real,parameter                       :: pi = 3.1416
!--- calc ---------
real                                    dlon
!----------------------
dlon = min( abs(lone-lonw), abs(360.0-(lone-lonw)))

cal_area_sphere = r**2.0 *dlon*pi/180.0 *(sin(latn/180.0*pi)-sin(lats/180.0*pi))
!----------------------
return
END FUNCTION cal_area_sphere
!******************************************************************
FUNCTION cal_f_phi_for_area(lat)
implicit none
!--- in ------------
real                                    lat   ! (degree)
!f2py intent(in)                        lat   ! (degree)
!--- out -----------
real                                    cal_f_phi_for_area
!f2py intent(out)                       cal_f_phi_for_area
!--- para ----------
real,parameter                       :: pi = 3.1416
real,parameter                       :: e2 = 0.00669447
real,parameter                       :: e  = 0.08181974
!--- calc ----------
real                                    phi
real                                    A, B
!-------------------
phi = lat/180.0 * pi   ! degree --> radian

A  = 0.5* sin(phi) / (1- e2*sin(phi)**2.0)
B  = 0.25/e *log( abs( (1+e*sin(phi))/(1-e*sin(phi)) ) )
cal_f_phi_for_area  = A + B
!-------------------
return
END FUNCTION cal_f_phi_for_area

!******************************************************************
FUNCTION cal_area_elip(lats, latn, lonw, lone)
!-------------------
! estimate area (km2) from Oki and Kanae 1997
!*** DO NOT USE!!  ******
!*** this is not symmetric in latitudinal direction
!***
!-------------------
implicit none
!--- in ------------
real                                    lats, latn, lonw, lone  ! (deg.)
!f2py intent(in)                        lats, latn, lonw, lone
!--- out -----------
real                                    cal_area_elip
!f2py intent(out)                       cal_area_elip
!--- para ----------
real,parameter                       :: a  = 6378.136
real,parameter                       :: pi = 3.1416
real,parameter                       :: e2 = 0.00669447
real,parameter                       :: e  = 0.08181974
!--- calc ----------
real                                    fs, fn
real                                    dlon
!-------------------
fn   = cal_f_phi_for_area(latn)
fs   = cal_f_phi_for_area(lats)
dlon = min( abs(lone-lonw), abs(360.0-(lone-lonw)))
!
cal_area_elip  = dlon *pi*a**2.0*(1.0-e2)/180.0 * (fn-fs)
!-------------------
return
END FUNCTION cal_area_elip

!******************************************************************
SUBROUTINE upscale_prep(a1lon_fin, a1lat_fin, a1lon_out, a1lat_out, globflag&
                           &, nlon_fin, nlat_fin, nlon_out, nlat_out&
                           &, a1xw_corres_fort, a1xe_corres_fort&
                           &, a1ys_corres_fort, a1yn_corres_fort&
                           &, a2areasw, a2arease, a2areanw, a2areane)
implicit none
!-------------------
! globflag =1: for global data ( left of the ix=1 is ix=nx)
!--- in ------------
integer                                 nlat_fin, nlon_fin, nlat_out, nlon_out
real,dimension(nlat_fin)             :: a1lat_fin
real,dimension(nlon_fin)             :: a1lon_fin
real,dimension(nlat_out)             :: a1lat_out
real,dimension(nlon_out)             :: a1lon_out 
!f2py intent(in)                        a1lat_fin, a1lon_fin, a1lat_out, a1lon_out
integer                                 globflag
!f2py intent(in)                        globflag
!--- out ------------
integer,dimension(nlon_fin)          :: a1xw_corres_fort, a1xe_corres_fort
!f2py intent(out)                       a1xw_corres_fort, a1xe_corres_fort
integer,dimension(nlat_fin)          :: a1ys_corres_fort, a1yn_corres_fort
!f2py intent(out)                       a1ys_corres_fort, a1yn_corres_fort
real,dimension(nlon_fin, nlat_fin)   :: a2areasw, a2arease, a2areanw, a2areane
!f2py intent(out)                       a2areasw, a2arease, a2areanw, a2areane
!--- calc -----------
integer                                 ifin, iout, ixfin, iyfin
integer                                 iout_start
integer                                 xw_corres, xe_corres, ys_corres, yn_corres
real,dimension(nlon_fin)             :: a1lonw_fin, a1lonm_fin, a1lone_fin
real,dimension(nlat_fin)             :: a1lats_fin, a1latm_fin, a1latn_fin
real,dimension(nlon_out)             :: a1lonw_out, a1lone_out
real,dimension(nlat_out)             :: a1lats_out, a1latn_out
real                                    lonw_fin, lone_fin, lonm_fin, lonw_out, lone_out
real                                    lats_fin, latn_fin, latm_fin, lats_out, latn_out
!--- parameter ------
real,parameter                       :: miss     = -9999.
integer,parameter                    :: miss_int = -9999
real,parameter                       :: pi = 3.1416
!--------------------
!-- init ----
a1xw_corres_fort    = miss_int
a1xe_corres_fort    = miss_int
a1ys_corres_fort    = miss_int
a1yn_corres_fort    = miss_int
a1lonw_out          = miss_int
a1lone_out          = miss_int
a1lats_fin          = miss
a1latn_fin          = miss
a1latm_fin          = miss
a1lonw_fin          = miss
a1lone_fin          = miss
a1lonm_fin          = miss
!---- a1lonw_out, a1lone_out ----
do iout = 2,nlon_out -1
  a1lonw_out(iout)   = (a1lon_out(iout) + a1lon_out(iout-1))*0.5
  a1lone_out(iout)   = (a1lon_out(iout+1) + a1lon_out(iout))*0.5
end do
if (globflag.eq.1)then
  a1lonw_out(1)        = (a1lon_out(nlon_out)-360.0 + a1lon_out(1))*0.5
  a1lone_out(1)        = (a1lon_out(1) + a1lon_out(2))*0.5
  a1lonw_out(nlon_out) = (a1lon_out(nlon_out) + a1lon_out(nlon_out-1))*0.5
  a1lone_out(nlon_out) = (a1lon_out(nlon_out) + a1lon_out(1)+360.0)*0.5
else
  a1lonw_out(1)        = a1lon_out(1) - (a1lon_out(2) - a1lon_out(1))*0.5
  a1lone_out(1)        = (a1lon_out(1) + a1lon_out(2))*0.5
  a1lonw_out(nlon_out) = (a1lon_out(nlon_out) + a1lon_out(nlon_out-1))*0.5
  a1lone_out(nlon_out) = a1lon_out(nlon_out) + (a1lon_out(nlon_out)-a1lon_out(nlon_out-1))*0.5
end if


!---- a1lats_out, a1latn_out ----
do iout = 2,nlat_out -1
  a1lats_out(iout)   = (a1lat_out(iout) + a1lat_out(iout-1))*0.5
  a1latn_out(iout)   = (a1lat_out(iout+1) + a1lat_out(iout))*0.5
end do
if (globflag.eq.1)then
  !a1lats_out(1)        =  a1lat_out(1) - (a1lat_out(2)-a1lat_out(1))*0.5
  a1lats_out(1)        = -90.0
  a1latn_out(1)        = (a1lat_out(1) + a1lat_out(2))*0.5
  a1lats_out(nlat_out) = (a1lat_out(nlat_out) + a1lat_out(nlat_out-1))*0.5
  !a1latn_out(nlat_out) = (a1lat_out(nlat_out) + (a1lat_out(nlat_out-1) + a1lat_out(nlat_out))*0.5)
  a1latn_out(nlat_out) = 90.0
else
  a1lats_out(1)        =  a1lat_out(1) - (a1lat_out(2)-a1lat_out(1))*0.5
  a1latn_out(1)        = (a1lat_out(1) + a1lat_out(2))*0.5
  a1lats_out(nlat_out) = (a1lat_out(nlat_out) + a1lat_out(nlat_out-1))*0.5
  a1latn_out(nlat_out) = (a1lat_out(nlat_out) + (a1lat_out(nlat_out) - a1lat_out(nlat_out-1))*0.5)

end if
!----- a1lonw_fin, a1lone_fin ----
do ifin = 2,nlon_fin -1
  a1lonw_fin(ifin)   = (a1lon_fin(ifin) + a1lon_fin(ifin-1))*0.5
  a1lone_fin(ifin)   = (a1lon_fin(ifin+1) + a1lon_fin(ifin))*0.5
end do
if (globflag.eq.1)then
  a1lonw_fin(1)        = (a1lon_fin(nlon_fin)-360.0 + a1lon_fin(1))*0.5
  a1lone_fin(1)        = (a1lon_fin(1) + a1lon_fin(2))*0.5
  a1lonw_fin(nlon_fin) = (a1lon_fin(nlon_fin) + a1lon_fin(nlon_fin-1))*0.5
  a1lone_fin(nlon_fin) = (a1lon_fin(nlon_fin) + a1lon_fin(1)+360.0)*0.5
else
  a1lonw_fin(1)        = a1lon_fin(1)- (a1lon_fin(2)-a1lon_fin(1))*0.5
  a1lone_fin(1)        = (a1lon_fin(1) + a1lon_fin(2))*0.5
  a1lonw_fin(nlon_fin) = (a1lon_fin(nlon_fin) + a1lon_fin(nlon_fin-1))*0.5
  a1lone_fin(nlon_fin) = a1lon_fin(nlon_fin) + (a1lon_fin(nlon_fin)-a1lon_fin(nlon_fin-1))*0.5
end if
!---- a1lats_fin, a1latn_fin ----
do ifin = 2,nlat_fin -1
  a1lats_fin(ifin)   = (a1lat_fin(ifin) + a1lat_fin(ifin-1))*0.5
  a1latn_fin(ifin)   = (a1lat_fin(ifin+1) + a1lat_fin(ifin))*0.5
end do
if (globflag.eq.1)then
  a1lats_fin(1)        = -90.0
  a1latn_fin(1)        = (a1lat_fin(1) + a1lat_fin(2))*0.5
  a1lats_fin(nlat_fin) = (a1lat_fin(nlat_fin) + a1lat_fin(nlat_fin-1))*0.5
  a1latn_fin(nlat_fin) = 90.0
else
  a1lats_fin(1)        =  a1lat_fin(1) - (a1lat_fin(2)-a1lat_fin(1))*0.5
  a1latn_fin(1)        = (a1lat_fin(1) + a1lat_fin(2))*0.5
  a1lats_fin(nlat_fin) = (a1lat_fin(nlat_fin) + a1lat_fin(nlat_fin-1))*0.5
  a1latn_fin(nlat_fin) =  a1lat_fin(nlat_fin) + (a1lat_fin(nlat_fin) - a1lat_fin(nlat_fin-1))*0.5
end if
!****************************************
!---- x -----
!if      (a1lone_fin(nlon_fin-1).lt.a1lonw_out(1))then
if      (a1lone_fin(nlon_fin).lt.a1lonw_out(1))then
  continue
!else if (a1lone_out(nlon_out).le.a1lonw_fin(2))then
else if (a1lone_out(nlon_out).le.a1lonw_fin(1))then
  continue
else

  iout_start  = 1
  !do ifin = 2, nlon_fin-1
  do ifin = 1, nlon_fin
    lonw_fin =  a1lonw_fin(ifin)
    lone_fin =  a1lone_fin(ifin)
    xw_corres         = miss_int
    xe_corres         = miss_int

    if      (lone_fin.lt.a1lonw_out(1))then
      cycle
    else if (lonw_fin.ge.a1lone_out(nlon_out))then
      exit
    end if

    !do iout = iout_start, iout_start + 1
    do iout = iout_start, iout_start + nlon_out
      lonw_out = a1lonw_out(iout)
      lone_out = a1lone_out(iout)
      if ((lonw_out .le. lonw_fin).and.(lonw_fin.lt.lone_out))then
        xw_corres = iout
        if (lone_fin .lt. lone_out)then
          xe_corres   = iout
          a1lonm_fin(ifin)  = lone_fin
        else
          xe_corres   = iout +1
          a1lonm_fin(ifin)  = lone_out
        end if
        exit
      end if
    end do
    a1xw_corres_fort(ifin)     = xw_corres
    a1xe_corres_fort(ifin)     = xe_corres
    iout_start                 = xe_corres
  end do
end if
!*** ifin=1 and last ******
if (globflag.eq.0)then
  !-- ifin = nlon_fin -----
  if   (a1xe_corres_fort(nlon_fin).gt.nlon_out)then
    a1xe_corres_fort(nlon_fin) = miss_int
    a1lonm_fin(nlon_fin)  = a1lone_out(nlon_out)
  else
    continue
  end if
  !------------------------
else
  !-- ifin = 1 ------------
  lonw_fin = a1lonw_fin(1)
  if (a1lonw_out(1).le.lonw_fin)then
    a1xw_corres_fort(1)     = 1
  else
    a1xw_corres_fort(1)     = nlon_out
  end if
  
  lone_fin = a1lone_fin(1)
  if (lone_fin .lt. a1lone_out(1))then
    a1xe_corres_fort(1) = 1
  else
    a1xe_corres_fort(1) = 2
  end if
  
  if (a1xw_corres_fort(1).eq.a1xe_corres_fort(1))then
    a1lonm_fin(1) = lone_fin
  else if (a1xw_corres_fort(1) .eq. nlon_out )then
    a1lonm_fin(1) = a1lonw_out(1)
  else
    a1lonm_fin(1) = a1lone_out(1)
  end if
  
  !-- ifin = nlon_fin -----
  lonw_fin = a1lonw_fin(nlon_fin)
  if (a1lonw_out(nlon_out) .le. lonw_fin)then
    a1xw_corres_fort(nlon_fin) = nlon_out
  else
    a1xw_corres_fort(nlon_fin) = nlon_out -1
  end if
  
  lone_fin = a1lone_fin(nlon_fin)
  if (lone_fin .lt. a1lone_out(nlon_fin))then
    a1xe_corres_fort(nlon_fin) = nlon_out
  else
    a1xe_corres_fort(nlon_fin) = 1
  end if
  
  if (a1xw_corres_fort(nlon_fin).eq.a1xe_corres_fort(nlon_fin))then
    a1lonm_fin(nlon_fin) = lone_fin
  else if (a1xw_corres_fort(nlon_fin) .eq. nlon_out )then
    a1lonm_fin(nlon_fin) = a1lone_out(nlon_out)
  else
    a1lonm_fin(nlon_fin) = a1lone_out(nlon_out-1)
  end if
end if
!****************************************
!---- y -----

!if      (a1latn_fin(nlat_fin-1).lt.a1lats_out(1))then  
if      (a1latn_fin(nlat_fin).lt.a1lats_out(1))then  
  continue
!else if (a1lats_out(nlat_out).le.a1lats_out(2))then
else if (a1lats_out(nlat_out).le.a1lats_out(1))then
  continue
else
  
  iout_start  = 1
  !do ifin = 2, nlat_fin-1
  do ifin = 1, nlat_fin
    lats_fin =  a1lats_fin(ifin)
    latn_fin =  a1latn_fin(ifin)
    ys_corres         = miss_int
    yn_corres         = miss_int
  
    if      (latn_fin.lt.a1lats_out(1))then
      cycle
    else if (lats_fin.ge.a1latn_out(nlat_out))then
      exit
    end if
  
    !do iout = iout_start, iout_start + 1
    do iout = iout_start, iout_start + nlat_out
      lats_out = a1lats_out(iout)
      latn_out = a1latn_out(iout)
      if ((lats_out .le. lats_fin).and.(lats_fin.lt.latn_out))then
        ys_corres = iout
        if (latn_fin .lt. latn_out)then
          yn_corres   = iout
          a1latm_fin(ifin)  = latn_fin
        else
          yn_corres   = iout +1
          a1latm_fin(ifin)  = latn_out
        end if
        exit
      end if
    end do
    a1ys_corres_fort(ifin)     = ys_corres
    a1yn_corres_fort(ifin)     = yn_corres
    iout_start                 = yn_corres
  end do
end if
!*** ifin=1 and last ******
if (globflag.eq.0)then
  !-- ifin = nlat_fin -----
  if   (a1yn_corres_fort(nlat_fin).gt.nlat_out)then
    a1yn_corres_fort(nlat_fin) = miss_int
    a1latm_fin(nlat_fin)  = a1latn_out(nlat_out)
  else
    continue
  end if
  !------------------------
else 
  !-- ifin = 1 ------------
  a1ys_corres_fort(1) = 1
  latn_fin = a1latn_fin(1)
  if (latn_fin .lt. a1latn_out(1))then
    a1yn_corres_fort(1) = 1
  else
    a1yn_corres_fort(1) = 2
  end if
  
  if (a1yn_corres_fort(1) .eq. 1)then
    a1latm_fin(1)  = a1latn_fin(1)
  else
    a1latm_fin(1)  = a1latn_out(1)
  end if
  
  !-- ifin = nlat_fin -----
  a1yn_corres_fort(nlat_fin) = nlat_out
  lats_fin = a1lats_fin(nlat_fin)
  if (a1lats_out(nlat_out) .le. a1lats_fin(nlat_fin))then
    a1ys_corres_fort(nlat_fin) = nlat_out
  else
    a1ys_corres_fort(nlat_fin) = nlat_out -1
  end if
  
  if (a1ys_corres_fort(nlat_fin) .eq. nlat_out)then
    a1latm_fin(nlat_fin)  = a1lats_fin(nlat_fin)
  else
    a1latm_fin(nlat_fin)  = a1lats_out(nlat_out)
  end if
end if
!***************************
! calc area
!--------------------

do iyfin = 1, nlat_fin
  lats_fin = a1lats_fin(iyfin)
  latn_fin = a1latn_fin(iyfin)
  latm_fin = a1latm_fin(iyfin)
  do ixfin = 1, nlon_fin
    lonw_fin = a1lonw_fin(ixfin)
    lone_fin = a1lone_fin(ixfin)
    lonm_fin = a1lonm_fin(ixfin)

    !!--------
    !a2areasw(ixfin, iyfin)  = cal_area_elip(lats_fin, latm_fin, lonw_fin, lonm_fin)
    !a2arease(ixfin, iyfin)  = cal_area_elip(lats_fin, latm_fin, lonm_fin, lone_fin)
    !a2areanw(ixfin, iyfin)  = cal_area_elip(latm_fin, latn_fin, lonw_fin, lonm_fin)
    !a2areane(ixfin, iyfin)  = cal_area_elip(latm_fin, latn_fin, lonm_fin, lone_fin)

    a2areasw(ixfin, iyfin)  = cal_area_sphere(lats_fin, latm_fin, lonw_fin, lonm_fin)
    a2arease(ixfin, iyfin)  = cal_area_sphere(lats_fin, latm_fin, lonm_fin, lone_fin)
    a2areanw(ixfin, iyfin)  = cal_area_sphere(latm_fin, latn_fin, lonw_fin, lonm_fin)
    a2areane(ixfin, iyfin)  = cal_area_sphere(latm_fin, latn_fin, lonm_fin, lone_fin)


    !--------
  end do
end do
!--------------------
return
END SUBROUTINE upscale_prep
!******************************************************************

end module
