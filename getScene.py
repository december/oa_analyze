import os
import csv

binnum = 32
namelist = os.listdir('../timeseries/')
scenedic = {}

for item in namelist:
	if not item[-4:] == '.csv':
		continue
	singlefile = list()
	csvfile = file('../timeseries/'+item)
	reader = csv.reader(csvfile)
	for line in reader:
		singlefile.append(line)
	csvfile.close()
	for line in singlefile:
		if line[3] != '1':
			continue
		if scenedic.has_key(line[5]):
			scenedic[line[5]] += 1
		else:
			scenedic[line[5]] = 1

scenedic = sorted(scenedic.iteritems(), key=lambda d:int(d[0]))

fw = open('../scene.csv', 'w')
for key in scenedic:
	s = str(key)
	k = s.split('\'')[1]
	v = s.split(',')[1][1:-1]
	fw.write(k)
	fw.write(',')
	fw.write(v)
	fw.write('\n')
fw.close()

print 'Finished.'
