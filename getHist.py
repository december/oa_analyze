import numpy as np
import matplotlib.pyplot as plt
import os
import csv

binnum = 32
namelist = os.listdir('../doubleline_text/')
pattern = {}
ptnum = [0, 0, 0, 0, 0]

def getHist(data):
	y = list()
	b = min(data)
	e = max(data)
	d = (e - b) * 1.0 / binnum
	if d == 0:
		return y
	for i in range(binnum):
		y.append(0)
	for item in data:
		index = int((item - b) / d)
		if index >= binnum:
			index = binnum - 1
		y[index] += 1
	n = len(data)
	for i in range(binnum):
		y[i] = y[i] * 1.0 / n
	return y

def getPattern(idnum, bhist, khist):
	n = len(bhist)
	bb = 0
	mb = 0
	bk = 0
	mk = 0
	for i in range(n):
		if bhist[i] >= 0.2:
			bb += 1
		if bhist[i] < 0.2 and bhist[i] >= 0.1:
			mb += 1
		if khist[i] >= 0.2:
			bk += 1
		if khist[i] < 0.2 and khist[i] >= 0.1:
			mk += 1
	if bb == 1 and mb == 0:
		pattern[idnum] = 'Coupon'
		ptnum[0] += 1
		return True
	if bb + mb >= 3:
		pattern[idnum] = 'Opera'
		ptnum[1] += 1
		return True
	if bk > 0 or mk >= 3:
		pattern[idnum] = 'In-Out'
		ptnum[2] += 1
		return True
	if bk == 0 and mk == 0:
		pattern[idnum] = 'School'
		ptnum[3] += 1
		return True
	return False

for item in namelist:
	if not item[-4:] == '.csv':
		continue
	name = item.split('_')[1]
	singlefile = list()
	csvfile = file('../doubleline_text/'+item)
	reader = csv.reader(csvfile)
	for line in reader:
		#print line
		singlefile.append(line)
	csvfile.close()
	bluelist = list()
	blklist = list()
	n = len(singlefile[0])
	flag = False
	for i in range(n):
		bluelist.append(int(singlefile[1][i]))
		blklist.append(int(singlefile[1][i]) - int(singlefile[2][i]))
		if int(singlefile[1][i]) < int(singlefile[2][i]):
			flag = True
			break
	if flag:
		continue
	bluehist = getHist(bluelist)
	blkhist = getHist(blklist)
	if len(bluehist) == 0 or len(blkhist) == 0:
		continue
	if not getPattern(name, bluehist, blkhist):
		pattern[name] = 'Unknown'
		ptnum[4] += 1

print ptnum
fw = open('../patternJudge.csv', 'w')
for key in pattern:
	fw.write(key)
	fw.write(',')
	fw.write(pattern[key])
	fw.write('\n')
fw.close()
