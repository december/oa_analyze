import numpy
import matplotlib.pyplot
import os


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

linefile = open('../lineId.csv', '')
for item in idlist:
