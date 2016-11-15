import matplotlib.pyplot as plt
import numpy as np
import csv
import sys

name = ['id','ds','rntype','srvtype','contype', 'custtype', 'nickname', 'vname', 'fans', 'post', 'intro']
rntype = [0,0,0,0,0]
srvtype = [0,0,0]
contype = [0,0,0,0,0]
custtype = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def makeInfo(s):
	temp = list()
	temp.append(s[0])
	temp.append(s[7])
	temp.append(s[10])
	temp.append(s[19])
	temp.append(s[24])
	temp.append(s[9])
	temp.append(s[20])
	temp.append(s[4])
	temp.append(s[23])
	temp.append(s[16])
	return temp

def makeStat(v):
	if v[1] != '' and int(v[1]) < 5 and int(v[1]) >= 0:
		rntype[int(v[1])] += 1
	if v[2] != '' and int(v[2]) < 3 and int(v[2]) >= 0:
		srvtype[int(v[2])] += 1		
	if v[3] != '' and int(v[3]) < 5 and int(v[3]) >= 0:
		contype[int(v[3])] += 1
	if v[4] != '' and int(v[4]) < 15 and int(v[4]) >= 0:
		custtype[int(v[4])] += 1

csv.field_size_limit(sys.maxsize)
csvfile = file('/mnt/data5/luyunfei/rawdata/Wechat_OA/10544_all_mod1k.csv', 'r')
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

print rntype
print srvtype
print contype
print custtype

