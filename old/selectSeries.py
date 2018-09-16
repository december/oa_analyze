import csv
import os

def inRange(time, events):
	#up_e = 400
	#down_e = 300
	up_t = 1.5 * 10 ** 7
	down_t = 1 * 10 ** 7
	std = 100
	if time >= down_t and time <= up_t:
	#if events >= down_e and events <= up_e and time >= down_t and time <= up_t:
		return events * 1.0 / std
	return 0

gooddic = {}
csvfile = file('../selectOA.csv', 'r')
reader = csv.reader(csvfile)
for line in reader:
	gooddic[line[0]] = float(line[1])
csvfile.close()

data = {}
namelist = os.listdir('../timeseries/')
for item in namelist:
	if not gooddic.has_key(item[:-4]):
		continue
	csvfile = file('../timeseries/'+item, 'r')
	reader = csv.reader(csvfile)
	temp = list()
	for line in reader:
		if int(line[3]) == 1:
			temp.append(int(line[2]))
	data[item[:-4]] = temp
	csvfile.close()

finallist = list()

fw = open('../LSMP/goodSeries.csv', 'w')
cnt = 0
small = 0
for key in data:
	data[key] = sorted(data[key])
	interval = inRange(data[key][-1] - data[key][0], len(data[key]))
	if interval < 1:
		continue
	#if interval < 1:
	#	small += 1
	cnt += 1
	fw.write(key)
	fw.write(',')
	fw.write(str(int(len(data[key]) / round(interval))))
	base = data[key][0]
	n = len(data[key])
	for i in range(n):
		if i > 0:
			while data[key][i] <= data[key][i-1]:
				data[key][i] += 0.001
		if i % round(interval) != 0:
			continue
		finallist.append(data[key][i]-base)
		fw.write(',')
		fw.write(str(data[key][i]-base))
	fw.write('\n')
fw.close()
print cnt
#print small

fw = open('../LSMP/finalSeries.csv', 'w')
finallist = sorted(finallist)
n = len(finallist)
fw.write('100')
fw.write(',')
fw.write(str(n))
for i in range(n):
	if i > 0:
		while finallist[i] <= finallist[i-1]:
			finallist[i] += 0.001
	fw.write(',')
	fw.write(str(finallist[i]))
fw.close()
