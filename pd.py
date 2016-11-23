import csv
import numpy as np
import pylab as pl

data = list()
infodic = {}
alist = list()
blist = list()
threshold = 0.05

csvfile = file('../rmse_ExpPL.csv')
reader = csv.reader(csvfile)
for line in reader:
	data.append(line)
csvfile.close()

for line in data:
	temp = list()
	temp.append(float(line[1]))
	temp.append(float(line[2]))
	infodic[line[0]] = temp

data = list()
csvfile = file('../params_exp.csv')
reader = csv.reader(csvfile)
for line in reader:
	data.append(line)
csvfile.close()

for line in data:
	if infodic.has_key(line[0]):
		infodic[line[0]].append(float(line[3].split('=')[1].split(' ')[0]))
		infodic[line[0]].append(float(line[7].split('=')[1].split(' ')[0]))

data = list()
csvfile = file('../params_pl.csv')
reader = csv.reader(csvfile)
for line in reader:
	data.append(line)
csvfile.close()

for line in data:
	if infodic.has_key(line[0]):
		infodic[line[0]].append(float(line[3].split('=')[1].split(' ')[0]))
		infodic[line[0]].append(float(line[11].split('=')[1].split(' ')[0]))

for key in infodic:
	if infodic[key][0] <= threshold:
		if infodic[key][3] < 0.01:
			alist.append(infodic[key][3])
	if infodic[key][1] <= threshold:
		if infodic[key][5] < 0.4:
			blist.append(infodic[key][5])

binnum = 64
b = min(alist)
e = max(alist)
bins = np.linspace(b, e, binnum)
print b
print e
print bins
pl.hist(np.array(alist), bins)
pl.savefig('alpha.png')
pl.cla()

b = min(blist)
e = max(blist)
bins = np.linspace(b, e, binnum)
pl.hist(np.array(blist), bins)
pl.savefig('beta.png')
pl.cla()

