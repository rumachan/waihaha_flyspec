#! /opt/local/epd-7.3.1/bin/python

#split flies of multiple scans into individual scans and plot angle vs concentration

#id, pcyear, pcmonth, pcday, pchour, pcminute, pcsecond, gpstime, gpslat, ns, gpslon, ew, gpsht, overload-0/1, digitisercounts, ?, ppmconc, angle, temp, battery, current
#2366 2014   11  8 10 30 00.299 212831.000 3906.3039 S  17540.8214  E  1404.5 0 26209.15 50 10.06 2  14.0 12.24  1.47
#2367 2014   11  8 10 30 00.736 212831.000 3906.3039 S  17540.8214  E  1404.5 0 34151.02 50 -19.49 4  14.0 12.24  1.47
#id column as index

import matplotlib
matplotlib.use('Agg') # this prevents the display
import matplotlib.pyplot as plt
import sys
import os

angle_last = 999

#input arguments
if (len(sys.argv) != 3):
  sys.exit("syntax fs_splitplot.py datafile outdir")
else:
  datafile = sys.argv[1]
  outdir = sys.argv[2]
  if not os.path.exists(outdir):
    os.makedirs(outdir)

with open(datafile) as f:
	for line in f.readlines():
		line.rstrip('\n')
		
		if len(line.split()) != 21:	#truncated line
			print 'short line in', datafile, ':', line
		else:	#do something
			angle = int(line.split()[17])
			conc = float(line.split()[16])
			oload = float(line.split()[13])
			if angle <= angle_last:	#new file
				if angle_last != 999:
					#plot results of previous scan
					fig = plt.figure(figsize=(15, 5))
					ax = fig.add_subplot(111)
					colors = []
                                        size = []
                                        for value in oloadplt:
                                          if value == 0:
                                            colors.append('r')
                                            size.append(0)
                                          else:
                                            colors.append('b')
                                            size.append(50)
					plt.plot(angleplt, concplt, color='red', linewidth=2)
                                        plt.scatter(angleplt, concplt, color=colors, s=size)
					plt.title(dt, fontsize=30)
					plt.tick_params(axis='both', which='major', labelsize=20)
					plt.savefig(pfile, dpi=200)
			
				angle_last = 0
				angleplt = []
				concplt = []
				oloadplt = []
				#get date and time for filename, pad to appropriate length
				year = line.split()[1]
				month = line.split()[2].zfill(2)
				day = line.split()[3].zfill(2)
				hour = line.split()[4].zfill(2)
				minute = line.split()[5].zfill(2)
				second = line.split()[6]
				dt = year + month + day + '_' + hour + minute + second[0:2]

				#output file and plot file
				ofile = outdir + '/' +'scan_' + dt + '.dat'
				pfile = outdir + '/' +'scan_' + dt + '.png'
				#print 'ofile:', ofile 
				of = open(ofile, 'w')
				of.write(line)

				#append angle and conc to array for plotting
				angleplt.append(angle)
				concplt.append(conc)
				oloadplt.append(oload)
				#update angle
				angle_last = angle
							
			else:	#existing file
				of.write(line)
				angleplt.append(angle)
				concplt.append(conc)
				oloadplt.append(oload)
				angle_last = angle
      
#plot results of final scan
fig = plt.figure(figsize=(15, 5))
ax = fig.add_subplot(111)
colors = []
size = []
for value in oloadplt:
  if value == 0:
    colors.append('r')
    size.append(0)
  else:
    colors.append('b')
    size.append(50)
plt.plot(angleplt, concplt, color='red', linewidth=2)
plt.scatter(angleplt, concplt, color=colors, s=size)
plt.title(dt, fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.savefig(pfile, dpi=100)
