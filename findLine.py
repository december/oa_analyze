import csv
import os

def isLine(t):
	n = len(t)
	dlist = list()
	for i in range(n-1):
		d = int(t[i+1]) - int(t[i])
		dlist.append(d)
	m = int(t[n-1])
	if m == 0:
		m += 1
	if len(dlist) == 0:
		return 0
	if (max(dlist) - min(dlist)) * 1.0 / m >= 0.05:
		return -1
	return (int(t[n-1]) - int(t[0])) * 1.0 / n / m

namelist = os.listdir('../doubleline_text/')
idlist = list()

for item in namelist:
	csvfile = file('../doubleline_text/'+item)
	reader = csv.reader(csvfile)
	temp = list()
	for line in reader:
		temp.append(line)
	a = isLine(temp[1])
	b = isLine(temp[2])
	if a >= 0 and b >= 0:
		infolist = list()
		infolist.append(item.split('_')[1])
		infolist.append(a)
		infolist.append(b)
		idlist.append(infolist)	
	csvfile.close()

linefile = open('../lineId.csv', 'w')
for line in idlist:
	linefile.write(str(line[0]))
	linefile.write(',')
	linefile.write(str(line[1]))
	linefile.write(',')
	linefile.write(str(line[2]))
	linefile.write('\n')
linefile.close()
