import matplotlib.pyplot as plt
import numpy as np
import csv

csvfile = file('11017_20160101_mod10w.csv', 'r')
reader = csv.reader(csvfile)
fanslist = list()
namelist = list()
timelist = list()
lastid = '-1'
temp = list()
first = True
flag = ''
lasttime = ''
for line in reader:
	if line[0][0] != '2':
		print line[0][0]
		continue
	if line[13] != lastid:
		if not first:
			namelist.append(name+flag)
			fanslist.append(temp)
			timelist.append(time+'-'+lasttime)
		else:
			first = False
		lastid = line[13]
		name = line[14]
		time = line[0]
		lasttime = line[0]
		flag = ''
		if time != '20160101':
			flag = '(NEW)'
		temp = list()
		temp.append(int(line[15]))
	else:
		temp.append(int(line[15]))
		lasttime = line[0]
		if line[14] != name and not line[14] == '':
			name = line[14]

n = len(namelist)
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
	plt.savefig('ocpic/'+str(i)+namelist[i]+'.png')
	plt.cla()


