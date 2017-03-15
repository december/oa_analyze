# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import csv

def isGood(t):
	if len(t) <= 10:
		return False
	if max(t) <= 100:
		return False
	if (max(t) - min(t)) * 1.0 / max(t) <= 0.05:
		return False
	return True

def mycmp(x, y):
	if x[13] < y[13]:
		return -1
	if x[13] == y[13]:
		if x[0] < y[0]:
			return -1
		if x[0] == y[0]:
			return 0
	return 1

csvfile = file('../../rawdata/Wechat_OA/11017_20160101_mod1k.csv', 'r')
reader = csv.reader(csvfile)
fanslist = list()
namelist = list()
timelist = list()
lastid = '-1'
temp = list()
first = True
flag = ''
uin = ''
lasttime = ''
total = 0
bad = 0

data = list()
for line in reader:
	data.append(line)
data.sort(cmp=mycmp)
print 'Finished sorting.'

orderfile = open('../../rawdata/Wechat_OA/ordered_11017', 'wb')
for line in data:
	for item in line:
		orderfile.write(item+' ')
	orderfile.write('\n')
orderfile.close()

for line in data:
	if line[0][0] != '2':
		print line[0][0]
		continue
	if line[13] != lastid:
		if not first:
			if isGood(temp):
				name = name.replace('/', '|')
				t = list()
				t.append(uin)
				t.append(name+flag)
				namelist.append(t)
				fanslist.append(temp)
				timelist.append(time+'-'+lasttime)
			else:
				bad += 1
		else:
			first = False
		lastid = line[13]
		name = line[14]
		time = line[0]
		lasttime = line[0]
		flag = ''
		if time != '20160101':
			flag = '(NEW)'
		uin = line[4]
		temp = list()
		temp.append(int(line[15]))
	else:
		temp.append(int(line[15]))
		lasttime = line[0]
		if line[14] != name and not line[14] == '':
			name = line[14]
	total += 1
	if total % 10000 == 0:
		print total

n = len(namelist)
print '!'+str(n)

idfile = open('../idlist', 'wb')
for i in range(n):
	idfile.write(namelist[i][0])
	idfile.write(' ')
	idfile.write(namelist[i][1])
	idfile.write('\n')
idfile.close()

print 'Finished writing.'

for i in range(n):
	m = len(fanslist[i])
	temp = list()
	for j in range(m):
		temp.append(j+1)
	x = np.array(temp)
	y = np.array(fanslist[i])
	plt.plot(x, y, 'o')
	plt.title(unicode(timelist[i], 'utf-8'))
	plt.xlabel(u'Time')
	plt.ylabel(u'FansNum')
	plt.savefig('../fansnum_id/'+str(i)+'_'+namelist[i][0]+'_'+namelist[i][1]+'.png')
	plt.cla()

print 'Finished.('+str(total)+' items in total, '+str(total-bad)+' good ones.)'
