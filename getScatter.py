import numpy
import matplotlib.pyplot
import csv

postnum = {}
csvfile = file('../oaInfo.csv', 'r')
reader = csv.reader(csvfile)
for line in reader:
	postnum[line[0]] = line[9]
csvfile.close()

k1 = list()
k2 = list()
p = list()
csvfile = file('../lineId.csv', 'r')
reader = csv.reader(csvfile)
for line in reader:
	if postnum.has_key(line[0]):
		p.append(int(postnum[line[0]]))
		k1.append(int(line[1]))
		k2.append(int(line[2]))
csvfile.close()

f1 = pyplot.figure(1)
pyplot.scatter(p, k1)

f2 = pyplot.figure(2)
pyplot.scatter(p, k2)
