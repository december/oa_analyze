import csv
import matplotlib.pyplot as plt
import numpy as np

peaklist = {}
csvfile = file('../peakdate.csv')
reader = csv.reader(csvfile)
for line in reader:
	n = len(line)
	temp = list()
	for i in range(1, n):
		temp.append(line[i])
	peaklist[line[0]] = temp
csvfile.close()

namelist = os.listdir('../doubleline_text/')

for item in namelist:
	idnum = item.split('_')[1]

	csvfile = file('../doubleline_text/'+item)
	reader = csv.reader(csvfile)

	csvfile.close()

