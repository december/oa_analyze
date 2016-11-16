import csv
import matplotlib.pyplot as plt
import numpy as np
import os

peakdic = {}
csvfile = file('../peakdate.csv')
reader = csv.reader(csvfile)
for line in reader:
	n = len(line)
	temp = list()
	for i in range(1, n):
		temp.append(line[i])
	peakdic[line[0]] = temp
csvfile.close()

namelist = os.listdir('../doubleline_text/')

for item in namelist:
	idnum = item.split('_')[1]
	if not peakdic.has_key(idnum):
		continue
	singlefile = list()
	csvfile = file('../doubleline_text/'+item)
	reader = csv.reader(csvfile)
	for line in reader:
		singlefile.append(line)
	csvfile.close()
	count = 0
	while count < len(peakdic[idnum]):
		idb = int(peakdic[idnum][count])
		ide = min(10, len(singlefile[0]))
		if count + 1 < len(peakdic[idnum]):
			ide = max(ide, int(peakdic[idnum][count+1]))
		x = list()
		y = list()
		r = list()
		for i in range(idb, ide - 1):
			if (int(singlefile[2][i]) > 0 and int(singlefile[2][i+1]) > 0):
				x.append(int(singlefile[2][i]))
				r.append(int(singlefile[2][i]))
				y.append(int(singlefile[2][i+1]))

		x = np.array(x)
		y = np.array(y)
		r = np.array(r)
		plt.plot(x, y, 'or')
		plt.plot(x, r, 'k')
		plt.title(idnum+': Peak '+str(count))
		plt.xlabel('Q(t)')
		plt.ylabel('Q(t+1)')
		plt.xscale('log')
		plt.yscale('log')
		plt.savefig('../Qcurve/'+idnum+'_'+str(count)+'.png')
		plt.cla()
		count += 1

print len(peakdic)
