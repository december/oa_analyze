import numpy
import matplotlib.pyplot as plt
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
		k1.append(float(line[1]))
		k2.append(float(line[2]))
csvfile.close()

f1 = plt.figure(1)
#plt.xscale('log')
ax = plt.gca()
#plt.scatter(p, k1)
ax.scatter(p, k1)
ax.sex_xscale('log')
plt.savefig('1.png')
plt.cla()

f2 = plt.figure(2)
#plt.xscale('log')
ax = plt.gca()
#plt.scatter(p, k2)
ax.scatter(p, k2)
ax.sex_xscale('log')
plt.savefig('2.png')
plt.cla()
