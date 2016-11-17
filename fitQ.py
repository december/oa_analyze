from lmfit import minimize, Parameters, Parameter, report_fit
import numpy as np
import os
import csv
import math

namelist = os.listdir('../doubleline_text/')
rmse_exp = list()
rmse_pl = list()

def isCoupon(golist):
	n = len(golist)
	'''
	if int(golist[0]) * 1.0 / int(golist[n-1]) > 0.05 and int(golist[0]) > 20:
		return 0 
	dlist = list()
	dlist.append(int(golist[0]))
	for i in range(1, n):
		d = int(golist[i]) - int(golist[i-1])
		dlist.append(d)
	for i in range(1, n):
		if d[i] > 4 * d[i-1] and d[i] > 20:
			return i
	return -1
	'''
	golist = [int(k) for k in golist]
	m = max(golist)
	for i in range(n):
		if golist[i] == m:
			return min(i - 1, 0)
	return 0

def calcExp(alpha, N, nsteps):
	model = list()
	for i in range(nsteps):
		model.append(N * (1 - math.exp(-1 * alpha * i)))
	return model

def exponential(params, tlist, glist):
	nsteps = max(tlist) + 1
	alpha = params['alpha'].value
	N = params['N'].value
	model = np.array(calcExp(alpha, N, nsteps))
	data = np.array(glist)
	try:
        return model-data
    except:
        print model
        print data
        return

def calcPL(beta, N, nsteps):
	model = list()
	for i in range(nsteps):
		model.append(N * (1 - math.pow(i, -1 * beta)))
	return model

def powerlaw(params, tlist, glist):
	nsteps = max(tlist) + 1
	beta = params['beta'].value
	N = params['N'].value
	model = np.array(calcPL(beta, N, nsteps))
	data = np.array(glist)
	try:
        return model-data
    except:
        print model
        print data
        return

def drawPic(tlist, glist, result, path, flag):
	nsteps = max(tlist) + 1
	rmse = 0
	if flag == 1:
		model = calcExp(result.params['alpha'].value, result.params['N'].value, nsteps)
		for i in range(nsteps):
			rmse += (glist[i] - model[i]) * (glist[i] - model[i])
		rmse_exp.append(math.sqrt(rmse * 1.0 / nsteps))
	else:
		model = calcPL(result.params['beta'].value, result.params['N'].value, nsteps)
		for i in range(nsteps):
			rmse += (glist[i] - model[i]) * (glist[i] - model[i])
		rmse_pl.append(math.sqrt(rmse * 1.0 / nsteps))
	m = np.array(model)
	g = np.array(glist)
	t = np.array(tlist)
	plt.plot(t, g, 'r+')
	plt.plot(t, m, 'k')
	plt.savefig(path)

fw1 = open('../params_exp.csv', 'w')
fw2 = open('../params_pl.csv', 'w')
count = 0
for item in namelist:
	name = item.split('_')[1]
	singlefile = list()
	csvfile = file('../doubleline_text/'+item)
	reader = csv.reader(csvfile)
	for line in reader:
		singlefile.append(line)
	csvfile.close()
	t = isCoupon(singlefile[2])
	if t < 0:
		continue
	tlist = list()
	glist = list()
	n = len(singlefile[2])
	base = 0
	if t > 0:
		base = int(singlefile[2][t])
	for i in range(t, n):
		tlist.append(i - t)
		glist.append(int(singlefile[2][i]) - base)
	if len(tlist) == 0:
		continue
	tlist = np.array(tlist)
	glist = np.array(glist)
	params = Parameters()
	params.add('N', value=int(singlefile[2][n-1]), min=0.0)
	params.add('alpha', value=0.01, min=0.0)
	params.add('beta', value=0.4, min=0.0)
	r1 = minimize(exponential, params, args=(tlist, glist))
	fw1.write(name+',')
	fw1.write(str(r1.params))
	fw1.write('\n')
	drawPic(tlist, glist, r1, '../fitpic_exp/'+name+'.png', 1)
	r2 = minimize(powerlaw, params, args=(tlist, glist))
	fw2.write(name+',')
	fw2.write(str(r2.params))
	fw2.write('\n')
	drawPic(tlist, glist, r2, '../fitpic_pl/'+name+'.png', 2)
	count += 1
	if count % 500 == 0:
		print count
fw1.close()
fw2.close()

exp_score = 0
pl_score = 0

fw = open('../rmse_ExpPL.csv', 'w')
n = len(rmse_exp)
for i in range(n):
	fw.write(namelist[i].split('_')[1])
	fw.write(',')
	fw.write(str(rmse_exp[i]))
	fw.write(',')
	fw.write(str(rmse_pl[i]))
	fw.write('\n')
	if rmse_exp[i] > rmse_pl[i]:
		pl_score += 1
	if rmse_exp[i] < rmse_pl[i]:
		exp_score += 1

print exp_score
print sum(rmse_exp) * 1.0 / len(rmse_exp)

print pl_score
print sum(rmse_pl) * 1.0 / len(rmse_pl)
