import matplotlib.pyplot as plt
import numpy as np
import csv
import os

gooddic = {}
csvfile = file('../selectOA.csv', 'r')
reader = csv.reader(csvfile)
for line in reader:
	gooddic[line[0]] = float(line[1])

fw = open('../goodOA.csv', 'w')
csvfile = file('../oaInfo.csv', 'r')
reader = csv.reader(csvfile)
setdic = {}
for line in reader:
	setdic[line[0]] = line[6]
	if gooddic.has_key(line[0]):
		l = len(line)
		fw.write(line[0])
		for i in range(1, l):
			fw.write(',')
			fw.write(line[i])
		fw.write('\n')
noidlist = list()
fw.close()

threshold = 0.95
select = list()

namelist = os.listdir('../sep_series/')
for item in namelist:
	if not gooddic.has_key(item[:-4]):
		continue
	csvfile = file('../sep_series/'+item, 'r')
	reader = csv.reader(csvfile)
	data = list()
	for line in reader:
		data.append(line)
	csvfile.close()
	
	timelist = [int(k) for k in data[0]]
	comelist = [int(k) for k in data[1]]
	golist = [int(k) for k in data[2]]
	onlist = [int(k) for k in data[3]]
	offlist = [int(k) for k in data[4]]
	onqlist = [int(k) for k in data[5]]
	offqlist = [int(k) for k in data[6]]
	t = np.array(timelist)
	c = np.array(comelist)
	g = np.array(golist)
	x = np.array(onlist)
	y = np.array(offlist)
	z = np.array(onqlist)
	w = np.array(offqlist)
	plt.plot(t, c, 'b')
	plt.plot(t, g, 'r')
	plt.plot(t, x, 'g')
	plt.plot(t, y, 'g--')
	'''
	plt.plot(t, z, 'm')
	plt.plot(t, w, 'm--')
	'''
	plt.xlabel(u'Time')
	plt.ylabel(u'Number')
	
	timelist = [int(k) for k in data[0]]
	t = np.array(timelist)
	margincome = list()
	margingo = list()
	n = len(data[3])
	for i in range(n):
		if int(data[3][i]) + int(data[4][i]) == 0:
			margincome.append(0)
			continue
		margincome.append((int(data[3][i]) - int(data[4][i])))
		#margingo.append((int(data[5][i]) - int(data[6][i])) * 1.0 / (int(data[5][i]) + int(data[6][i])))
	mc = np.array(margincome)
	#mg = np.array(margingo)
	#plt.ylim(-1, 1)
	plt.plot(t, mc, 'm')
	#plt.plot(t, mg, 'r')

	name = 'noname'
	if setdic.has_key(item[:-4]):
		name = setdic[item[:-4]]
	else:
		noidlist.append(item[:-4])
	plt.savefig('../difference_pic/'+item[:-4]+'_'+name+'.png')
	plt.cla()
