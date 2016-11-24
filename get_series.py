import matplotlib.pyplot as plt
import numpy as np
import csv
import datetime
import time
import os

def makeString(line):
	s = line[0] + ',' + line[4] + ',' + line[10] + ',' + line[13] + ',' + line[14] + ',' + line[15] + '\n'
	return s

idlist = list()
namelist = os.listdir('../doubleline_text/')
for item in namelist:
	idlist.append(item.split('_')[1])
idset = set(idlist)

data = list()
csvfile = file('../ordered_10059.csv', 'r')
reader = csv.reader(csvfile)
for line in reader:
	data.append(line)
csvfile.close()

'''
csvfile = file('../intialnum.csv', 'r')
reader = csv.reader(csvfile)
initiallist = list()
for line in reader:
	initiallist.append(line)

begin = 0
initsize = len(initiallist)
'''

first = True
lastid = -1
cnt = 0
for line in data:
	cnt += 1
	if line[0][0] != '2':
		print line[0][0]
		continue
	line = line[0].split(' ')
	if line[4] != lastid:
		if not line[4] in idset:
			continue
		if not first:
			single.close()
		else:
			first = False
		single = open('../timeseries/'+line[4]+'.csv', 'w')
		single.write(makeString(line))
		lastid == line[4]
	else:
		if not line[4] in idset:
			continue
		single.write(makeString(line))
	if cnt % 10000 == 0:
		print cnt
single.close()
