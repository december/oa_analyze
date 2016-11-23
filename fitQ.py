#-*- coding: utf-8 -*-
from lmfit import minimize, Parameters, Parameter, report_fit
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
import math

namelist = os.listdir('../doubleline_text/')
rmse_exp = list()
rmse_pl = list()
nlist = list()
namedic = {}

def isCoupon(golist):
	n = len(golist)
	if int(golist[n-1]) == 0:
		return -1
	if int(golist[0]) * 1.0 / int(golist[n-1]) > 0.05 and int(golist[0]) > 20:
		return 0 
	dlist = list()
	dlist.append(int(golist[0]))
	for i in range(1, n):
		d = int(golist[i]) - int(golist[i-1])
		dlist.append(d)
	for i in range(1, n):
		if dlist[i] > 4 * dlist[i-1] and dlist[i] > 20:
			return i
	return 0
	'''
	golist = [int(k) for k in golist]
	m = max(golist)
	for i in range(n):
		if golist[i] == m:
			return max(i - 1, 0)
	return 0
	'''

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
		return model - data
	except:
		print model
		print data
		return

def calcPL(beta, N, nsteps):
	model = list()
	for i in range(nsteps):
		model.append(N * (1 - math.pow(i + 1, -1 * beta)))
	return model

def powerlaw(params, tlist, glist):
	nsteps = max(tlist) + 1
	beta = params['beta'].value
	N = params['N'].value
	model = np.array(calcPL(beta, N, nsteps))
	data = np.array(glist)
	try:
		return model - data
	except:
		print model
		print data
		return

def drawPic(tlist, glist, blist, res1, res2, path, base):
	if max(glist) == 0:
		return
	nsteps = max(tlist) + 1
	'''
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
	'''
	rmse = 0
	model1 = calcExp(res1.params['alpha'].value, res1.params['N'].value, nsteps)
	for i in range(nsteps):
		rmse += (glist[i] - model1[i]) * (glist[i] - model1[i])
	r1 = math.sqrt(rmse * 1.0 / nsteps) / max(glist)
	rmse_exp.append(r1)
	rmse = 0
	model2 = calcPL(res2.params['beta'].value, res2.params['N'].value, nsteps)
	for i in range(nsteps):
		rmse += (glist[i] - model2[i]) * (glist[i] - model2[i])
	r2 = math.sqrt(rmse * 1.0 / nsteps) / max(glist)
	rmse_pl.append(r2)
	nlist.append(path.split('/')[2].split('_')[0])
	s1 = 'EX: N='+str(round(res1.params['N'].value, 1))+' A='+str(res1.params['alpha'].value)+' R='+str(r1)
	s2 = 'PL: N='+str(round(res2.params['N'].value, 1))+' B='+str(res2.params['beta'].value)+' R='+str(r2)
	m = len(model1)
	for i in range(m):
		model1[i] += base
		model2[i] += base
		glist[i] += base
	m1 = np.array(model1)
	m2 = np.array(model2)
	g = np.array(glist)
	t = np.array(tlist)
	b = np.array(blist)
	if not len(blist) == 0:
		plt.plot(t, b, 'b+')
	plt.plot(t, g, 'r+')
	plt.plot(t, m1, 'k', label=s1)
	plt.plot(t, m2, 'g', label=s2)
	plt.legend(loc='lower right')
	leg = plt.gca().get_legend()
	ltext  = leg.get_texts()
	plt.setp(ltext, fontsize='small')
	#plt.text(1, max(glist), 'N:   alpha:    RMSE:    (Exp)')
	#plt.text(1, 0.9 * max(glist), 'N:   alpha:    RMSE:    (PL)')
	plt.savefig(path)
	plt.cla()

csvfile = file('../oaInfo.csv')
reader = csv.reader(csvfile)
for line in reader:
	if len(line[0]) == 8:
		namedic[line[1]] = line[6]
	else:
		namedic[line[0]] = line[6]
csvfile.close()

fw1 = open('../params_exp.csv', 'w')
fw2 = open('../params_pl.csv', 'w')
count = 0
for item in namelist:
	if not item[-4:] == '.csv':
		continue
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
	blist = list()
	n = len(singlefile[2])
	base = 0
	baseb = 0
	if t > 0:
		base = int(singlefile[2][t-1])
		baseb = int(singlefile[1][t-1])
	for i in range(t, n):
		tlist.append(i - t)
		glist.append(int(singlefile[2][i]) - base)
		blist.append(int(singlefile[1][i]))
	if len(tlist) < 3:
		continue
	tlist = np.array(tlist)
	glist = np.array(glist)
	blist = np.array(blist)
	params = Parameters()
	#
	params.add('N', value=int(singlefile[2][n-1])-base, min=0.0, max=max(int(singlefile[1][n-1]) - baseb, int(singlefile[2][n-1]) - base))
	params.add('alpha', value=0.01, min=0.0)
	params.add('beta', value=0.15, min=0.0)
	#print len(tlist)
	#print len(glist)
	r1 = minimize(exponential, params, args=(tlist, glist))
	fw1.write(name+',')
	fw1.write(str(r1.params))
	fw1.write('\n')
	#drawPic(tlist, glist, r1, '../fitpic_exp/'+name+'.png', 1)
	r2 = minimize(powerlaw, params, args=(tlist, glist))
	fw2.write(name+',')
	fw2.write(str(r2.params))
	fw2.write('\n')
	nickname = 'Unknown'
	if namedic.has_key(name):
		nickname = namedic[name]
	#blist = list()
	drawPic(tlist, glist, blist, r1, r2, '../fitpic_all_max/'+name+'_'+nickname+'.png', base)
	count += 1
	if count % 100 == 0:
		print count
	#if count >= 500:
	#	break
	#except:
	#	print name
fw1.close()
fw2.close()

exp_score = 0
pl_score = 0

fw = open('../rmse_ExpPL.csv', 'w')
n = len(rmse_exp)
for i in range(n):
	fw.write(nlist[i])
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
