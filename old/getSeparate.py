import matplotlib.pyplot as plt
import numpy as np
import datetime
import csv
import math
import os

online = [57, 17, 39, 56, 75, 101, 9, 42, 8]
offline = [30, 51, 45]
ignore = []
errordic = {}

def checkSign(line):
	if line[3] == '-1':
		return 0
	if int(line[5]) in online:
		return 1
	if int(line[5]) in offline:
		return 2
	return 3

def writeArray(fw, array, n):
	fw.write(str(array[0]))
	for i in range(1, n):
		fw.write(',')
		fw.write(str(array[i]))
	fw.write('\n')

csvfile = file('../oaInfo.csv', 'r')
reader = csv.reader(csvfile)
setdic = {}
for line in reader:
	setdic[line[0]] = line[6]
noidlist = list()

csvfile = file('../KCresult.csv', 'r')
reader = csv.reader(csvfile)
data = list()
for line in reader:
	data.append(line)
csvfile.close()
label = {}
for line in data:
	label[line[0]] = line[1]

namelist = os.listdir('../timeseries/')
for item in namelist:
	if item[-4:] != '.csv':
		continue
	csvfile = file('../timeseries/'+item, 'r')
	reader = csv.reader(csvfile)
	data = list()
	for line in reader:
		data.append(line)
	csvfile.close()
	data.sort(key=lambda x:x[2])
	on = 0
	off = 0
	come = 0
	go = 0
	onq = 0
	offq = 0
	onlist = list()
	offlist = list()
	onqlist = list()
	offqlist = list()
	comelist = list()
	golist = list()
	ondic = {}
	offdic = {}
	alldic = {}
	lasttime = data[0][0]
	for line in data:
		if line[0] != lasttime:
			onlist.append(on)
			offlist.append(off)
			comelist.append(come)
			golist.append(go)
			onqlist.append(onq)
			offqlist.append(offq)
			lasttime = line[0]
		sign = checkSign(line)
		if sign == 0:
			go += 1
			if alldic.has_key(line[4]):
				alldic.pop(line[4])
			else:
				if errordic.has_key(item[:-4]):
					errordic[item[:-4]] += 1
				else:
					errordic[item[:-4]] = 1
			if ondic.has_key(line[4]):
				onq += 1
				ondic.pop(line[4])
			if offdic.has_key(line[4]):
				offq += 1
				offdic.pop(line[4])
		else:
			come += 1
			alldic[line[4]] = 1
		if sign == 1:
			on += 1
			ondic[line[4]] = 1
		if sign == 2:
			off += 1
			offdic[line[4]] = 1
	onlist.append(on)
	offlist.append(off)
	comelist.append(come)
	golist.append(go)
	onqlist.append(onq)
	offqlist.append(offq)
	timelist = list()
	n = len(golist)
	for i in range(n):
		timelist.append(i)
	fw = open('../sep_series/'+item.split('.')[0]+'.csv', 'w')
	writeArray(fw, timelist, n)
	writeArray(fw, comelist, n)
	writeArray(fw, golist, n)
	writeArray(fw, onlist, n)
	writeArray(fw, offlist, n)
	writeArray(fw, onqlist, n)
	writeArray(fw, offqlist, n)
	fw.close()
	t = np.array(timelist[:100])
	c = np.array(comelist[:100])
	g = np.array(golist[:100])
	x = np.array(onlist[:100])
	y = np.array(offlist[:100])
	z = np.array(onqlist[:100])
	w = np.array(offqlist[:100])
	plt.plot(t, c, 'b')
	plt.plot(t, g, 'r')
	plt.plot(t, x, 'g')
	plt.plot(t, y, 'g--')
	plt.plot(t, z, 'm')
	plt.plot(t, w, 'm--')
	plt.xlabel(u'Time')
	plt.ylabel(u'Number')
	uin = item.split('.')[0]
	name = 'noname'
	if setdic.has_key(uin):
		name = setdic[uin]
	else:
		noidlist.append(uin)
	labelnum = 'n'
	if label.has_key(item.split('.')[0]):
		labelnum = label[item.split('.')[0]]
	plt.savefig('../sep_pic/'+labelnum+'_'+uin+'_'+name+'.png')
	plt.cla()
fw = open('../errorOA.csv', 'w')
for key in errordic:
	fw.write(key)
	fw.write(',')
	fw.write(str(errordic[key]))
	fw.write('\n')
fw.close()
print len(errordic)
