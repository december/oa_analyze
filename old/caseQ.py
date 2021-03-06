import csv
import matplotlib.pyplot as plt
import numpy as np

filename = ['61_2390862830_20150702-20161110', '102_2391481967_20150710-20161111', '139_2391977476_20150729-20161110', '187_2392865803_20150725-20161107', '283_2394682337_20150703-20161109', '778_3005305954_20150702-20161102', '812_3006647916_20150704-20161109', '957_3010769514_20151218-20160628', '1039_3012969893_20160527-20161111', '1115_3014844253_20160316-20161111', '1181_3016955899_20160517-20161107', '1216_3017733559_20151026-20161108', '1262_3018782403_20151229-20161102', '1302_3019818286_20160223-20161110', '1329_3070521718_20150702-20161111', '1357_3070930488_20150709-20161111', '1387_3071493793_20150702-20161110', '1393_3071641349_20151202-20161111', '1424_3072473844_20151020-20161104', '1554_3075449889_20150704-20161111', '1574_3075961350_20160225-20161111', '1591_3076356162_20150705-20161111', '1644_3077565523_20150704-20161110', '1706_3078940386_20151008-20161111', '1778_3080512655_20151029-20161104']
N = [480, 2500, 1200, 1200, 60, 430, 730, 550, 7000, 350, 255, 970, 230, 230, 3900, 7200, 630, 9200, 700, 1500, 520, 1500, 1130, 56500, 1000]
T = [327, 188, 137, 227, 367, 0, 329, 0, 0, 0, 10, 60, 24, 92, 294, 146, 182, 20, 2, 263, 20, 291, 198, 153, 56]

fixnum = 1

n = len(filename)
for i in range(n):
	csvfile = file('../doubleline_text/'+filename[i]+'.csv')
	name = filename[i].split('_')[1]
	reader = csv.reader(csvfile)
	single = list()
	for line in reader:
		single.append(line)
	csvfile.close()
	x = list()
	y = list()
	z = list()
	d = 0
	if not T[i] == 0:
		d = int(single[2][i-1])
	for j in range(T[i], len(single[2])):
		if N[i] > int(single[2][j]):
			x.append(j+1)
			y.append(np.log(j+1))
			z.append(np.log(1 - (int(single[2][j]) - d) * 1.0 / (N[i] - d) / fixnum))
		else:
			break
	x = np.array(x)
	y = np.array(y)
	z = np.array(z)
	plt.plot(x, z, 'or')
	plt.title(name)
	plt.xlabel('t')
	plt.ylabel('ln(1-Q(t)/N)')
	plt.savefig('../coupon/'+name+'_t.png')
	plt.cla()

	plt.plot(y, z, 'or')
	plt.title(name)
	plt.xlabel('ln(t)')
	plt.ylabel('ln(1-Q(t)/N)')
	plt.savefig('../coupon/'+name+'_ln(t).png')
	plt.cla()

