import matplotlib.pyplot as plt
import numpy as np
import csv
import datetime
import time
import math

def isGood(c, g, t):
	'''
	if t == '20150701':
		return False
	'''
	if len(c) <= 10:
		return False
	if max(c) <= 100 and max(g) <= 100:
		return False
	return True

def mycmp(x, y):
	if x[4] < y[4]:
		return -1
	if x[4] == y[4]:
		if x[0] < y[0]:
			return -1
		if x[0] == y[0]:
			return 0
	return 1

def delta(begin, now):
	b = datetime.datetime.strptime(begin, '%Y%m%d')
	n = datetime.datetime.strptime(now, '%Y%m%d')
	d = n - b
	return d.days

def makeDelta(ts):
	temp = list()
	temp.append(ts[0])
	m = len(ts)
	for i in range(1, m):
		temp.append(ts[i] - ts[i-1])
	return temp

csvfile = file('/mnt/data5/luyunfei/rawdata/Wechat_OA/10059_all_mod1k.csv', 'r')
reader = csv.reader(csvfile)
comelist = list()
namelist = list()
golist = list()
timelist = list()
timestring = list()
lastid = '-1'
lasttime = ''
temp = list()
first = True
data = list()
total = 0
bad = 0

for line in reader:
	data.append(line)
data.sort(cmp=mycmp)
print 'Finshed sorting.'

orderfile = open('../ordered_10059.csv', 'wb')
for line in data:
	for item in line:
		orderfile.write(item+' ')
	orderfile.write('\n')
orderfile.close()

'''
csvfile = file('../intialnum.csv', 'r')
reader = csv.reader(csvfile)
initiallist = list()
for line in reader:
	initiallist.append(line)

begin = 0
initsize = len(initiallist)
'''

for line in data:
	if line[0][0] != '2':
		print line[0][0]
		continue
	if line[4] != lastid:
		if not first:
			tempcome.append(come)
			tempgo.append(go)
			if isGood(tempcome, tempgo, time):
				namelist.append(lastid)
				comelist.append(tempcome)
				golist.append(tempgo)
				timelist.append(temptime)
				timestring.append(time+'-'+lasttime)
			else:
				bad += 1
		else:
			first = False
		lastid = line[4]
		time = line[0]
		lasttime = line[0]
		tempcome = list()
		tempgo = list()
		temptime = list()
		temptime.append(0)
		come = 0
		'''
		while begin < initsize:
			if initiallist[begin][0] == lastid:
				come = int(initiallist[begin][1])
				break
			if initiallist[begin][0] > lastid:
				break
			begin += 1
		'''
		go = 0
		if int(line[13]) == 1:
			come += 1
		else:
			go += 1
	else:
		if line[0] != lasttime:
			tempcome.append(come)
			tempgo.append(go)
			lasttime = line[0]
			d = delta(time, line[0])
			n = len(temptime) - 1
			while temptime[n] < d - 1:
				temptime.append(temptime[n]+1)
				tempcome.append(come)
				tempgo.append(go)
				n += 1
			temptime.append(d)
			if int(line[13]) == 1:
				come += 1
			else:
				go += 1			
		else:
			if int(line[13]) == 1:
				come += 1
			else:
				go += 1
	total += 1
	if total % 10000 == 0:
		print total

n = len(namelist)

peakdate = {}
for i in range(n):
	m = len(comelist[i])
	temp = list()
	for j in range(1, m):
		d = comelist[j] - comelist[j-1]
		base = comelist[j-1]
		if base == 0:
			base += 1
		if d * 1.0 / base >= 0.25 and d > 25:
			temp.append(j)
	peakdate[namelist[i]] = temp
peakfile = open('../peakdate.csv', 'wb')
for k in peakdate:
	peakfile.write(k)
	for item in peakdate[k]:
		peakfile.write(',')
		peakfile.write(str(item))
	peakfile.write('\n')
peakfile.close()

total = len(data)
count = 0
holdtime = {}
while count < total:
	if data[count][0][0] != '2':
		count += 1
		continue
	if peakfile.has_key(data[count][4]):
		crid = data[count][4]
		begintime = line[0]
		cindex = 0
		htdic = {}
		tempht = list()
		peaknum = len(peakfile[crid])
		while cindex < peaknum:
			while delta(begintime, data[count][0]) < peakfile[crid][cindex]:
				count += 1
			peaktime = data[count][0]
			newcount = count
			while newcount < total and data[newcount][4] == crid:
				if int(data[newcount][13]) == 1 and data[newcount][0] == peaktime:
					htdic[data[newcount][4]] = peaktime
				if int(data[newcount][13]) == -1 and htdic.has_key(date[newcount][4]):
					tempht.append(delta(htdic[data[newcount][4]], data[newcount][0]))
					htdic.pop(data[newcount][4])
				if len(htdic) == 0 and data[newcount][0] != peaktime:
					break;
				newcount += 1
			cindex += 1
		holdtime[crid] = tempht
		while crid == data[count][4]:
			count += 1
	else:
		count += 1

binnum = 10
for key in ht:
	b = math.log(min(ht[key]) + 1)
	e = math.log(max(ht[key]) + 1)
	if b == e:
		continue
	d = (b - e) * 1.0 / (binnum - 1)
	x = list()
	y = list()
	for i in range(binnum):
		x.append(round(math.pow.(10, b + d * (0.5 + i))))
		y.append(0)
	for item in ht[key]:
		y[int((log(item+1) - b) / d)] += 1
	m = len(ht[key])
	for i in range(binnum):
		y[binnum] = y[binnum] * 1.0 / m
	x = np.array(x)
	y = np.array(y)
	plt.plot(x, y, 'o')
	plt.title(str(min(ht[key]))+' days to '+str(max(ht[key]))+' days')
	plt.xlabel('Holding Time')
	plt.ylabel('Distribution')
	plt.xscale('log')
	plt.savefig('../holdtime/'+str(k)+'.png')
	plt.cla()

for i in range(n):
	#singlefile = open('../dldata/'+str(i)+'_'+namelist[i]+'.csv')
	#singlefile.write()

	x = np.array(comelist[i])
	dx = np.array(makeDelta(comelist[i]))
	y = np.array(golist[i])
	dy = np.array(makeDelta(golist[i]))
	z = np.array(timelist[i])
	plt.plot(z, x, 'b')
	plt.plot(z, y, 'r')
	plt.title(unicode(timestring[i], 'utf-8'))
	plt.xlabel(u'Time')
	plt.ylabel(u'Number')
	plt.savefig('../doubleline_all/'+str(i)+'_'+namelist[i]+'.png')
	plt.cla()

	plt.scatter(z, dx, 'b')
	plt.scatter(z, dy, 'r')
	plt.title(unicode(timestring[i], 'utf-8'))
	plt.xlabel(u'Time')
	plt.ylabel(u'Speed')
	plt.savefig('../delta_all/'+str(i)+'_'+namelist[i]+'.png')
	plt.cla()

