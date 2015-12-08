
       subroutine gridsintp(
     i rlonin,rlatin,
     i r3in,
     i rlon,rlat,
     i miss,
     o r3out,
     h nxin,nyin,nzin,nx,ny)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c HJKIM@UCCHM
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      implicit none

      integer           nx, ny
      integer           nxin,nyin,nzin
      real*8            miss
cf2py intent(in) miss

      real*8            rlon(nx), rlat(ny)
cf2py intent(in) rlon,rlat

      real*8            rlonin(nxin),rlatin(nyin)
cf2py intent(in) rlonin,rlatin

      real*8            r3in(nxin,nyin,nzin)
cf2py intent(in) r3in(nxin,nyin,nzin)

      real*8            r3out(nx,ny,nzin)
cf2py intent(out) r3out(nxin,nyin,nzin)

      integer           k
      real*8            r2tmpin(nxin,nyin), r2tmpout(nx,ny)
      integer           igrdxl(nx), igrdxr(nx)
      integer           igrdyu(ny), igrdyl(ny)


      call meshxy(
     i  rlonin,rlatin,rlon,rlat,
     o  igrdxl, igrdxr, igrdyl, igrdyu,
     h  nxin,nyin,nx,ny)

      do k=1, nzin
        r2tmpin = r3in(:,:,k)

        call gridintp(
     i    rlonin,rlatin,r2tmpin,rlon,rlat,miss,
     i    igrdxl, igrdxr, igrdyl, igrdyu,
     o    r2tmpout,
     h    nxin,nyin,nx,ny)

        r3out(:,:,k) = r2tmpout

      enddo
      end


       subroutine gridintp(
     i rlonin,rlatin,
     i r2in,
     i rlon,rlat,
     i miss,
     i igrdxl, igrdxr, igrdyl, igrdyu,
     o r2out,
     h nxin,nyin,nx,ny)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c HJKIM@IIS.U-TOKYO
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

      implicit none

      integer           nx, ny
      integer           nxin, nyin
      real*8            miss
cf2py intent(in) miss

      real*8            rlon(nx), rlat(ny)
cf2py intent(in) rlon, rlat

      real*8            rlonin(nxin), rlatin(nyin)
cf2py intent(in) rlonin,rlatin

      real*8          r2in(nxin,nyin)
cf2py intent(in) r2in

      real*8          r2out(nx,ny)
cf2py intent(out) r2out

      integer           i, j
      integer           igrdxl(nx), igrdxr(nx)
      integer           igrdyu(ny), igrdyl(ny)

      real*8            lon, lon1, lon2
      real*8            lat, lat1,lat2

      real*8            rgetara
      real*8            area,areasum
      real*8            dat

cccccccccccccccccccccccccccccccccccccccccccccccc
c LON  0  -> 360
c LAT -90 -> 90
c
c           lon1                 lon2
c             :                   :      
c             |                   |      
c           O3|                   |O4      
c  lat2 ------o-------------------o------ lat2
c             | A3         : A4   |      
c             |            :      |      
c             |            :      |      
c             |            :      |      
c             |''''''''''''I''''''|      
c             |  I(lat,lon):      |      
c             |            :      |      
c             | A1         : A2   |      
c  lat1 ------o-------------------o------ lon1
c           O1|                   |O2      
c             |                   |      
c             :                   :      
c           lon1                 lon2
cccccccccccccccccccccccccccccccccccccccccccccccc

      do i=1, nx
        do j=1, ny

          areasum = 0.0
          r2out(i,j) = 0.0
          
          lon  = rlon(i)
          lon1 = rlonin(igrdxl(i))
          lon2 = rlonin(igrdxr(i))

          lat  = rlat(j)
          lat1 = rlatin(igrdyl(j))
          lat2 = rlatin(igrdyu(j))
 
c          write(*,*) i,j, lon1,lon,lon2,lat1,lat,lat2
ccc A1 ccc
          dat  = r2in(igrdxr(i),igrdyu(j))
          area = rgetara(lon1,lon,lat1,lat)

          if (dat.NE.miss) then
            areasum  = areasum + area
            r2out(i,j) = r2out(i,j) + dat*area
          endif

ccc A2 ccc
          dat  = r2in(igrdxl(i),igrdyu(j))
          area = rgetara(lon,lon2,lat1,lat)

          if (dat.NE.miss) then
            areasum  = areasum + area
            r2out(i,j) = r2out(i,j) + dat*area
          endif

ccc A3 ccc
          dat  = r2in(igrdxr(i),igrdyl(j))
          area = rgetara(lon1,lon,lat,lat2)

          if (dat.NE.miss) then
            areasum  = areasum + area
            r2out(i,j) = r2out(i,j) + dat*area
          endif

ccc A4 ccc
          dat  = r2in(igrdxl(i),igrdyl(j))
          area = rgetara(lon,lon2,lat,lat2)

          if (dat.NE.miss) then
            areasum  = areasum + area
            r2out(i,j) = r2out(i,j) + dat*area
          endif

          if (areasum.GT.0) then
            r2out(i,j) = r2out(i,j)/areasum
          else
            r2out(i,j) = miss
          endif

        enddo
      enddo
      end


      subroutine meshxy(
     i rlonin,rlatin,rlon,rlat,
     o igrdxl, igrdxr, igrdyl, igrdyu,
     h nxin,nyin,nx,ny)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      implicit none

      integer nx, ny
      integer nxin,nyin

      real*8 rlon(nx),rlat(ny)
cf2py intent(in) rlon, rlat
      real*8 rlonin(nxin), rlatin(nyin)
cf2py intent(in) rlonin, rlatin
      integer igrdxl(nx),igrdxr(nx)
cf2py intent(out) igrdxl, igrdxr
      integer igrdyl(ny),igrdyu(ny)
cf2py intent(out) igrdyl, igrdyu

      integer i, j, minarg
      real*8 tmplon(nxin),tmplat(nyin)

ccccccccccccccccccc
ccccc gird x
ccccccccccccccccccc

      do i = 1, nx

        tmplon = rlonin-rlon(i)

        minarg = minloc( abs(tmplon), DIM=1 )

        if ( tmplon(minarg).GE.0. ) then
          igrdxl(i) = minarg-1
          igrdxr(i) = minarg
        else
          igrdxl(i) = minarg
          igrdxr(i) = minarg+1
        endif

        if ( igrdxl(i).EQ.0    ) igrdxl(i) = nxin
        if ( igrdxr(i).GT.nxin ) igrdxr(i) = 1

      enddo

ccccccccccccccccccc
ccccc gird y
ccccccccccccccccccc

      do j = 1, ny
        tmplat = rlatin-rlat(j)

        if ( rlat(j).LT.0. ) then
          igrdyu(j) = minloc( tmplat, DIM=1, MASK=(tmplat>=0) )

          if ( igrdyu(j).EQ.1 ) then
            igrdyl(j) = 1
          else
            igrdyl(j) = igrdyu(j)-1
          endif

        else
          igrdyl(j) = maxloc( tmplat, DIM=1, MASK=(tmplat<0) )

          if ( igrdyl(j).EQ.nyin ) then
            igrdyu(j) = nyin
          else
            igrdyu(j) = igrdyl(j)+1
          endif

        endif


      enddo

      end
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


      double precision function rgetara(rlon1, rlon2, rlat1, rlat2)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
cto   calculate area of 1 degree longitude box at each latitude
cby   algorithm by T. Oki, mathematics by S. Kanae, mod by nhanasaki
con   26th Oct 2003
cat   IIS,UT
c
c     rlat1, rlat2 : latitude -90.0 (south pole) to 90.0 (north pole)
c     returns arealat : in m^2
c     by approximated equation
cccccccccccccccccccccccccccccccccccccccccccccccccc
      implicit none
c
      real*8           rlon1  
      real*8           rlon2   
      real*8           rlat1    
      real*8           rlat2 
cf2py intent(in) rlon1, rlon2, rlat1, rlat2
cf2py intent(ou) rgetara

      real*8           rpi    
      double precision dpi     
      double precision de       
      double precision de2 
      double precision drad 
      double precision dfnc1 
      double precision dfnc2  
      double precision dsin1   
      double precision dsin2    
c
      data             de2/0.00669447/
      data             rpi/3.141592653589793238462643383/
      data             dpi/3.141592653589793238462643383/
      data             drad/6378136/
cccccccccccccccccccccccccccccccccccccccccccccccccc
      de=sqrt(de2)
c
      if ((rlat1.gt.90).or.(rlat1.lt.-90).or.
     $    (rlat2.gt.90).or.(rlat2.lt.-90)) then
        write(6,*) 'rgetara: latitude out of range.'
        write(*,*) 'rlon1(east) : ',rlon1
        write(*,*) 'rlon2(west) : ',rlon2
        write(*,*) 'rlat1(north): ',rlat1
        write(*,*) 'rlat1(south): ',rlat2
        rgetara = 0.0
      else
        dsin1 = dble(sin(rlat1 * rpi/180))
        dsin2 = dble(sin(rlat2 * rpi/180))
c
        dfnc1 = dsin1*(1+(de*dsin1)**2/2)
        dfnc2 = dsin2*(1+(de*dsin2)**2/2)
c
c        if ((rlon2-rlon1).LT.0) then
c        write(*,*) 'negative',mod(mod(rlon2,360.)-mod(rlon1,360.),360.)
c          rgetara = real(dpi*drad**2*(1-de**2)/180*(dfnc1-dfnc2))
c     $         *(360.+mod(mod(rlon2,360.)-mod(rlon1,360.),360.))
c        else
c          rgetara = real(dpi*drad**2*(1-de**2)/180*(dfnc1-dfnc2))
c     $         *(mod(mod(rlon2,360.)-mod(rlon1,360.),360.))
c        endif
          rgetara = dble(dpi*drad**2*(1-de**2)/180*(dfnc1-dfnc2))
     $         *(rlon2-rlon1)
      end if
cccccccccccccccccccccccccccccccccccccccccccccccccc
c Sign has been changed - to +.'
cccccccccccccccccccccccccccccccccccccccccccccccccc
      if (rgetara.lt.0.0) then
        rgetara = - rgetara
      end if
c
      end

