lstr = ["aa\nbb","cc\ndd"]
#---------------------
nline = len(lstr[0].strip().split("\n"))
ddat = {}
for i in range(nline):
  ddat[i] = []
#---------------------
for strdat in lstr:
  lines  = strdat.split("\n")
  for i, line in enumerate(lines):
    ddat[i].append(line)
#---------------------
lout = []
for i in range(nline):
  lout.append(",".join(ddat[i]))
#---------------------
sout = "\n".join(lout)
print sout


