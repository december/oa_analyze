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
	if postnum.has_key(line[0]) and int(postnum[line[0]]) <= 250:
		p.append(int(postnum[line[0]]))
		k1.append(float(line[1]))
		k2.append(float(line[2]))
csvfile.close()

f1 = plt.figure(1)
#plt.xscale('log')
ax = plt.gca()
#plt.scatter(p, k1)
ax.scatter(p, k1)
#ax.set_xscale('log')
ax.set_xlim(0, 250)
#ax.set_yscale('log')
ax.set_ylim(0, 2)
plt.savefig('1.png')
plt.cla()

f2 = plt.figure(2)
#plt.xscale('log')
ax = plt.gca()
#plt.scatter(p, k2)
ax.scatter(p, k2)
#ax.set_xscale('log')
ax.set_xlim(0, 250)
#ax.set_yscale('log')
ax.set_ylim(0, 2)
plt.savefig('2.png')
plt.cla()
