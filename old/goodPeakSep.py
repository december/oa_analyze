import numpy as np
import csv
import os

gooddic = {}
csvfile = file('../selectOA.csv', 'r')
reader = csv.reader(csvfile)
for line in reader:
	gooddic[line[0]] = float(line[1])
csvfile.close()

onpeakdate = {}
offpeakdate = {}
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
	onlist = [int(k) for k in data[3]]
	temp = list()
	m = len(onlist)
	for i in range(1, m):
		d = onlist[i] - onlist[i-1]
		base = onlist[i-1]
		if base == 0:
			base += 1
		if d * 1.0 / base >= 0.25 and d > 25:
			temp.append(i)
	if len(temp) > 0:
		onpeakdate[item[:-4]] = temp

	offlist = [int(k) for k in data[4]]
	temp = list()
	m = len(offlist)
	for i in range(1, m):
		d = offlist[i] - offlist[i-1]
		base = offlist[i-1]
		if base == 0:
			base += 1
		if d * 1.0 / base >= 0.25 and d > 25:
			temp.append(i)
	if len(temp) > 0:
		offpeakdate[item[:-4]] = temp

fw = open('../peakdate_good_online.csv', 'wb')
for k in onpeakdate:
	fw.write(k)
	for item in onpeakdate[k]:
		fw.write(',')
		fw.write(str(item))
	fw.write('\n')
fw.close()

fw = open('../peakdate_good_offline.csv', 'wb')
for k in offpeakdate:
	fw.write(k)
	for item in offpeakdate[k]:
		fw.write(',')
		fw.write(str(item))
	fw.write('\n')
fw.close()

