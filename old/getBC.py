import os
import csv
import shutil

namelist = os.listdir('../doubleline_init/')
idlist = list()
for item in namelist:
	idlist.append(item.split('_')[1].split('.')[0])

basic = {}
csvfile = file('../oaInfo.csv', 'r')
reader = csv.reader(csvfile)
for line in reader:
	basic[line[0]] = line[2]+'/'

prefix = '../basic_category/'
n = len(idlist)
count = 0
error = 0
for i in range(n):
	count += 1
	if basic.has_key(idlist[i]):
		shutil.copyfile('../doubleline_init/'+namelist[i], prefix+basic[idlist[i]]+namelist[i])
	else:
		error += 1
print 'finished: '+str(count-error)
print 'error: '+str(error) 	
