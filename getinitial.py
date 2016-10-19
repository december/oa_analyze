import matplotlib.pyplot as plt
import numpy as np
import csv

infolist = list()

csvfile = file('../../rawdata/Wechat_OA/11017_20160101_mod1k.csv', 'r')
reader = csv.reader(csvfile)
for line in reader:
	if line[0] == '20160102':
		infolist.append(line[4]+','+line[15])

infolist.sort()

orderfile = open('intialnum.csv', 'wb')
for line in infolist:
	orderfile.write(line)
	orderfile.write('\n')
orderfile.close()
