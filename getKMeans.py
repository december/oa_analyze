import matplotlib.pyplot as plt
import sklearn.cluster as sc
import numpy as np
import datetime
import csv
import math
import os

scale = 100
peak = 100
peaktime = 50

csvfile = file('../KCresult.csv', 'r')
reader = csv.reader(csvfile)
data = list()
for line in reader:
	data.append(line)
csvfile.close()
label = {}
for line in data:
	label[line[0]] = line[1]

def getDelta(series):
	#print series[0]
	#array = series.split(',')
	array = [int(k) for k in series]
	newarray = list()
	newarray.append(array[0])
	n = len(array)
	for i in range(1, n):
		newarray.append(array[i] - array[i-1])
	return newarray

def getScale(series):
	n = len(series)
	unit = n * 1.0 / scale
	newarray = list()
	cur = 0
	for i in range(scale):
		before = int(math.floor(cur))
		after = int(math.floor(cur + unit))
		if after >= n:
			temp = series[before] * (before + 1 - cur)
			for j in range(before + 1, n):
				temp += series[j]
			newarray.append(temp)
			break
		if before == after:
			newarray.append(unit * series[before])
			cur += unit
			continue
		if before + 1 == after:
			newarray.append(series[before] * (after - cur) + series[after] * (cur + unit - after))
			cur += unit
			continue
		temp = series[before] * (before + 1 - cur) + series[after] * (cur + unit - after)
		for j in range(before + 1, after):
			temp += series[j]
		cur += unit
		newarray.append(temp)
	return newarray

def getShift(series):
	realmax = max(series)
	if realmax == 0:
		return series
	newarray = list()
	n = len(series)
	#print n
	pos = -1
	for i in range(n):
		if realmax == series[i]:
			pos = i
		series[i] = series[i] * 1.0 * peak / realmax
	for i in range(n):
		index = i - peaktime + pos
		if index < 0:
			index += scale
		if index >= scale:
			index -= scale 
		newarray.append(series[index])
	return newarray

namelist = os.listdir('../sep_series/')
nlist = list()
dataset = list()
for item in namelist:
	if item[-4:] != '.csv':
		continue
	csvfile = file('../sep_series/'+item, 'r')
	reader = csv.reader(csvfile)
	data = list()
	for line in reader:
		data.append(line)
	csvfile.close()
	d1 = list()
	n = len(data[0])
	if n < 40:
		continue
	nlist.append(item[:-4])
	for line in data:
		d1.append(getDelta(line))
	#print item
	#print d1[1]
	d2 = list()
	for line in d1:
		d2.append(getScale(line))
	#print d2[1]
	d3 = list()
	for line in d2:
		d3.append(getShift(line))
	
	#print d2[1]
	#print d2[1]
	#print d3[1]
	merge = list()
	fw = open('../cluster_series/'+label[item[:-4]]+'_'+item[:-4]+'.csv', 'w')
	for i in range(1, 7):
		for j in range(scale):
			fw.write(str(d3[i][j]))
			if j < scale - 1:
				fw.write(',')
			merge.append(d3[i][j])
		fw.write('\n')
	fw.close()
	dataset.append(merge)
d = np.array(dataset)
km = sc.KMeans().fit(d)
#print len(namelist)
#print len(km.labels_)
n = len(nlist)
fw = open('../KCresult.csv', 'w')
for i in range(n):
	fw.write(nlist[i])
	fw.write(',')
	fw.write(str(km.labels_[i]))
	fw.write('\n')
fw.close()
