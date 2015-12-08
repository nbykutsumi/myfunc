f2py -m grids -c  --fcompiler=gfortran --build-dir ./build ./_gridsintr.f

! default compiler (= ifort) ** segmentation fault for 0.25deg interpolation
!f2py -m grids -c  --build-dir ./build ./_gridsintr.f

