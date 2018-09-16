import matplotlib.pyplot as plt
import numpy as np
import csv
import os

errordic = {}
csvfile = file('../errorOA.csv', 'r')
reader = csv.reader(csvfile)
for line in reader:
	errordic[line[0]] = int(line[1])

threshold = 0.95
select = list()

namelist = os.listdir('../sep_series/')
for item in namelist:
	if item[-4:] != '.csv':
		continue
	csvfile = file('../sep_series/'+item, 'r')
	reader = csv.reader(csvfile)
	data = list()
	for line in reader:
		data.append(line)
	csvfile.close()
	ratio = 0
	n = len(data[0])
	if int(data[1][0]) == 0:
		continue
	if errordic.has_key(item[:-4]) and errordic[item[:-4]] <= int(data[1][-1]) * threshold:
		continue
	for i in range(n):
		ratio += (int(data[3][i]) + int(data[4][i])) * 1.0 / int(data[1][i])
	if ratio / n >= threshold:
		temp = list()
		temp.append(item[:-4])
		temp.append(ratio / n)
		select.append(temp)
fw = open('../selectOA.csv', 'w')
for item in select:
	fw.write(item[0])
	fw.write(',')
	fw.write(str(item[1]))
	fw.write('\n')
fw.close()
print len(select)
