import matplotlib.pyplot as plt
import numpy as np
import csv

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


csvfile = file('../../Data/Wechat_OA/10059_20160101_mod1k.csv', 'r')
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

for line in reader:
	data.append(line)
data.sort(mycmp)
print 'Finshed sorting.'

orderfile = open('../../Data/Wechat_OA/ordered_10059', 'wb')
for line in data:
	orderfile.write(line)
	orderfile.write('\n')
orderfile.close()

for line in data:
	if line[0][0] != '2':
		print line[0][0]
		continue
	if line[4] != lastid:
		if not first:
			tempcome.append(come)
			tempgo.append(go)
			if isGood(tempcome, tempgo):
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
		go = 0
		if int(line[13]) == 1:
			come += 1
		else:
			go += 1
	else:
		if line[0] != lasttime:
			tempcome.append(come)
			tempgo.append(go)
			come = 0
			go = 0
			lasttime = line[0]
			d = delta(time, line[0])
			n = len(temptime) - 1
			while temptime[n] < d - 1:
				temptime.append(temptime[n]+1)
				tempcome.append(0)
				tempgo.append(0)
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

for i in range(n):
	x = np.array(comelist[i])
	y = np.array(golist[i])
	z = np.array(timelist[i])
	plt.plot(x, z, 'ob')
	plt.plot(y, z, 'or')
	plt.title(unicode(timestring[i], 'utf-8'))
	plt.xlabel(u'Time')
	plt.ylabel(u'Number')
	plt.savefig('../../Data/Wechat_OA/doubleline/'+str(i)+'_'+namelist[i]+'.png')
	plt.cla()

