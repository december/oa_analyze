import matplotlib.pyplot as plt
import numpy as np
import datetime
import csv
import math
import os

online = [57, 17, 39, 56, 75, 101, 9, 42, 8]
offline = [30, 51, 45]
ignore = []

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
			if ondic.has_key(line[4]):
				onq += 1
				ondic.pop(line[4])
			if offdic.has_key(line[4]):
				offq += 1
				offdic.pop(line[4])
		else:
			come += 1
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
	plt.plot(t, z, 'm')
	plt.plot(t, w, 'm--')
	plt.xlabel(u'Time')
	plt.ylabel(u'Number')
	labelnum = 'n'
	if label.has_key(item.split('.')[0]):
		labelnum = label[item.split('.')[0]]
	plt.savefig('../sep_pic/'+labelnum+'_'+item.split('.')[0]+'.png')
	plt.cla()

