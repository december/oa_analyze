import matplotlib.pyplot as plt
import numpy as np
import csv

name = ['id','ds','rntype','srvtype','contype', 'custtype', 'nickname', 'vname', 'fans', 'post', 'intro']
rntype = [0,0,0,0,0]
srvtype = [0,0,0]
contype = [0,0,0,0,0]
custtype = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def makeInfo(s):
	temp = list()
	temp.append(s[0])
	temp.append(s[11])
	temp.append(s[14])
	temp.append(s[23])
	temp.append(s[30])
	temp.append(s[13])
	temp.append(s[24])
	temp.append(s[9])
	temp.append(s[27])
	temp.append(s[19])
	return temp

def makeStat(v):
	if int(v[1]) < 5 and int(v[1]) >= 0:
		rntype[int(v[1])] += 1
	if int(v[2]) < 3 and int(v[2]) >= 0:
		rntype[int(v[2])] += 1		
	if int(v[3]) < 5 and int(v[3]) >= 0:
		rntype[int(v[3])] += 1
	if int(v[4]) < 15 and int(v[4]) >= 0:
		rntype[int(v[4])] += 1

csv.field_size_limit(sys.maxsize)
csvfile = file('../../rawdata/Wechat_OA/10544_20160101_mod1k.csv', 'r')
reader = csv.reader(csvfile)
info = {}
for line in reader:
	if line[10] == '1':
		if info.has_key(line[1]):
			if line[0] > info[line[1]][0]:
				info[line[1]] = makeInfo(line)
		else:
			info[line[1]] = makeInfo(line)
	else:
		if info.has_key(line[1]):
			if line[0] > info[line[1]][0]:
				del info[line[1]]

file = open('../oaInfo.csv','wb')
for k in info:
	makeStat(info[k])
	file.write(k)
	for p in info[k]:
		file.write(',')
		file.write(p)
	file.write('\n')
file.close()
