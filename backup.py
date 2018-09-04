import subprocess
import socket

distHost = 'utsumi@mizu.iis.u-tokyo.ac.jp'
distPath = '/home/utsumi/Backup/bin'
dist = '%s:%s/'%(distHost, distPath)

hostname = socket.gethostname()
if hostname == 'mizu':
    srcPath  = '/home/utsumi/mnt/wellshare/bin/myfunc'
elif hostname=='well':
    srcPath  = '/media/disk2/share/bin/myfunc'

lcmd = ['rsync','-avr',srcPath, dist]
print lcmd
subprocess.call(lcmd)
