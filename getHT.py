# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import datetime
import csv
import math
import os

online = [57, 17, 39, 56, 75, 101, 9, 42, 8]
offline = [30, 51, 45]

def delta(begin, now):
	b = datetime.datetime.strptime(begin, '%Y%m%d')
	n = datetime.datetime.strptime(now, '%Y%m%d')
	d = n - b
	return d.days

def getReady(timeline, binnum):
	empty = list()
	if len(timeline) == 0:
		return empty, empty
	b = math.log(min(timeline))
	e = math.log(max(timeline))
	if b == e:
		return empty, empty
	d = (e - b) * 1.0 / (binnum - 1)
	x = list()
	y = list()
	for i in range(binnum):
		x.append(round(math.pow(math.e, b + d * (0.5 + i))))
		#x.append(b + d * (0.5 + i))
		y.append(0)
	for item in timeline:
		y[int((math.log(item) - b) / d)] += 1
	#数量除以bin的宽度
	for i in range(binnum):
		y[i] = y[i] * 1.0 / (math.pow(math.e, b + d * (i+1)) - math.pow(math.e, b + d * i))
	#或直接每秒画散点图
	m = len(timeline)
	
	cnt = binnum - 1
	while cnt >= 0:
		if y[cnt] == 0:
			y.pop(cnt)
			x.pop(cnt)
		else:
			y[cnt] = y[cnt] * 1.0 / m
		cnt -= 1
	
	#for i in range(binnum):
	#	y[i] = y[i] * 1.0 / m
	x = np.array(x)
	y = np.array(y)
	return x, y

csvfile = file('../peakdate.csv', 'r')
reader = csv.reader(csvfile)
data = list()
for line in reader:
	data.append(line)
csvfile.close()

peakdate = {}
for line in data:
	peakdate[line[0]] = line[1:]

namelist = os.listdir('../timeseries/')
holdtime = {}
ontime = {}
offtime = {}

for item in namelist:
	name = item.split('.')[0]
	if not peakdate.has_key(name):
		continue
	csvfile = file('../timeseries/'+item, 'r')
	reader = csv.reader(csvfile)
	data = list()
	for line in reader:
		data.append(line)
	csvfile.close()
	data.sort(key=lambda x:x[2])
	n = len(data)
	cnt = 0
	begintime = data[0][0]
	index = 0
	peaknum = len(peakdate[name])
	#print name
	#print peakdate[name]
	#print n
	while index < peaknum:
		while delta(begintime, data[cnt][0]) < int(peakdate[name][index]):
			cnt += 1
		peaktime = data[cnt][0]
		newcount = cnt
		htdic = {}
		ondic = {}
		offdic = {}
		tempht = list()
		tempon = list()
		tempoff = list()
		while newcount < n:
			#print newcount
			if int(data[newcount][3]) == 1 and data[newcount][0] == peaktime:
				htdic[data[newcount][4]] = int(data[newcount][2])
				if int(data[newcount][5]) in online:
					ondic[data[newcount][4]] = int(data[newcount][2])
				if int(data[newcount][5]) in offline:
					offdic[data[newcount][4]] = int(data[newcount][2])
			if int(data[newcount][3]) == -1 and htdic.has_key(data[newcount][4]):
				d = int(data[newcount][2]) - htdic[data[newcount][4]]
				if d > 0:
					tempht.append(d)
					htdic.pop(data[newcount][4])
					if ondic.has_key(data[newcount][4]):
						tempon.append(d)
						ondic.pop(data[newcount][4])
					if offdic.has_key(data[newcount][4]):
						tempoff.append(d)
						offdic.pop(data[newcount][4])
			if len(htdic) == 0 and data[newcount][0] != peaktime:
				break;
			newcount += 1
		index += 1
		holdtime[data[0][1]+'_'+str(index)] = tempht
		ontime[data[0][1]+'_'+str(index)] = tempon
		offtime[data[0][1]+'_'+str(index)] = tempoff
		#print tempht
print 'Finished calculating.'

binnum = 15
for key in holdtime:
	x, y = getReady(holdtime[key], binnum)
	if len(x) > 0:
		plt.plot(x, y, 'b')
	else:
		continue
	x, y = getReady(ontime[key], binnum)
	if len(x) > 0:
		plt.plot(x, y, 'g')
	x, y = getReady(offtime[key], binnum)
	if len(x) > 0:
		plt.plot(x, y, 'm')
	plt.title(str(len(x)) + ': ' + str(min(holdtime[key]))+' to '+str(max(holdtime[key])))
	plt.xlabel('Holding Time')
	plt.ylabel('Distribution')
	plt.xscale('log')
	plt.yscale('log')
	plt.savefig('../holdtime_seplog/'+str(key)+'.png')
	plt.cla()
print 'Finished holding time.'
