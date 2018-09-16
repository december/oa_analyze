#-*- coding: utf-8 -*-
from lmfit import minimize, Parameters, Parameter, report_fit
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
import math

namelist = list()
rmse = list()

def SIRdecayMultiImpulse(gamma=0.05, alpha=1.0, beta=0.05, G=200, n=40, nsteps=100, lambdaval=list(), deltaval=list()):
    totSteps=nsteps
    pseq = [0 for i in range(totSteps)]
    aseq = [0 for i in range(totSteps)]
    nseq = [0 for i in range(totSteps)]
    Pt =  [0 for i in range(totSteps)]
    At =  [0 for i in range(totSteps)]
    Nt =  [0 for i in range(totSteps)]
    qt =  [0 for i in range(totSteps)]
    n=int(n)
    pseq[0]=n
    Pt[0]=n
    myRes=list()
    #qt[0]=gamma
    for i in range(0,totSteps):
        qt[i]=gamma*((i+2)**(1-alpha)-(i+1)**(1-alpha))/(1-alpha)
    #print qt
    Nt[0]=n*qt[0]
    At[0]=Pt[0]-Nt[0]
    aseq[0]=At[0]
    for t in range(1,totSteps):
        S=max(0, G-Pt[t-1])
        pseq[t]=S*beta*At[t-1]/G
        for order in range(len(deltaval)):
            if t == deltaval[order]:
                pseq[t] += lambdaval[order]
        Pt[t]=Pt[t-1]+pseq[t]
        aseq[t]=pseq[t]
        for j in range(0,t):
            tmp=aseq[j]*qt[t-j]
            aseq[j]=aseq[j]-tmp
            nseq[t]=nseq[t]+tmp
        Nt[t]=Nt[t-1]+nseq[t]
        At[t]=At[t-1]+pseq[t]-nseq[t]

    myRes.append(Pt)
    #myRes.append(At)
    myRes.append(Nt)
    return myRes

def params2fcnvalMulti(params,nsteps,peaks):
    beta=params['beta'].value
    alpha=params['alpha'].value
    gamma=params['gamma'].value
    G=params['G'].value
    n=params['n'].value
    lambdaval=list()
    deltaval=list()
    for i in range(peaks):
        #if len(params) - 5 < 2 * (i + 1):
        #    break
        lambdaval.append(params['lambdaval'+str(i)].value)
        deltaval.append(params['delta'+str(i)].value)
    #nsteps=x.max()+1
    res=SIRdecayMultiImpulse(gamma,alpha,beta,G,n,nsteps,lambdaval,deltaval)
    return res

def fcn2minMultiImpulse(params,time,series,p):
    x1=time[0]
    x2=time[1]
    #Predict People
    nsteps=max(max(x1),max(x2))+1
    #nsteps=max(max(x1),max(x2))+11
    #print nsteps

    res=params2fcnvalMulti(params,nsteps,p)
    plist=list()
    nlist=list()
    for i in x1:
        plist.append(res[0][int(i)])
    for i in x2:
        nlist.append(res[1][int(i)])
    model=np.array(plist+nlist)
    d1=list(series[0])
    d2=list(series[1])
    data_f=np.array(d1+d2)
    try:
        return model-data_f
    except:
        print model
        print data_f
        print res
        return

def calcRMSE(real, model, nsteps):
	rmse = 0
	for i in range(nsteps):
		rmse += (real[i] - model[i]) * (real[i] - model[i])
	return math.sqrt(rmse * 1.0 / nsteps)

def drawPic(t, x, y, z, w, res1, res2, path, peak1, peak2):
	#if max(glist) == 0:
	#	return
	nsteps = max(t) + 1
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
	model_on = params2fcnvalMulti(res1.params, nsteps, peak1)
	model_off = params2fcnvalMulti(res2.params, nsteps, peak2)
	temp = list()
	temp.append(calcRMSE(x, model_on[0], nsteps))
	temp.append(calcRMSE(z, model_on[1], nsteps))
	temp.append(calcRMSE(y, model_off[0], nsteps))
	temp.append(calcRMSE(w, model_off[1], nsteps))
	rmse.append(temp)

	s1 = 'On-Join:' + str(round(temp[0], 2))
	s2 = 'On-Quit:' + str(round(temp[1], 2))
	s3 = 'Off-Join' + str(round(temp[2], 2))
	s4 = 'Off-Quit' + str(round(temp[3], 2))

	plt.plot(t, x, 'b+')
	plt.plot(t, y, 'g+')
	plt.plot(t, z, 'r+')
	plt.plot(t, w, 'm+')
	plt.plot(t, model_on[0], 'b', label=s1)
	plt.plot(t, model_off[0], 'g', label=s2)
	plt.plot(t, model_on[1], 'r', label=s3)
	plt.plot(t, model_off[1], 'm', label=s4)

	plt.legend(loc='best')
	leg = plt.gca().get_legend()
	ltext  = leg.get_texts()
	plt.setp(ltext, fontsize='small')
	#plt.text(1, max(glist), 'N:   alpha:    RMSE:    (Exp)')
	#plt.text(1, 0.9 * max(glist), 'N:   alpha:    RMSE:    (PL)')
	plt.savefig(path)
	plt.cla()

gooddic = {}
csvfile = file('../selectOA.csv', 'r')
reader = csv.reader(csvfile)
for line in reader:
	gooddic[line[0]] = float(line[1])
csvfile.close()

namedic = {}
csvfile = file('../oaInfo.csv')
reader = csv.reader(csvfile)
for line in reader:
	if len(line[0]) == 8:
		namedic[line[1]] = line[6]
	else:
		namedic[line[0]] = line[6]
csvfile.close()

onpeak = {}
csvfile = file('../peakdate_good_online.csv', 'r')
reader = csv.reader(csvfile)
for line in reader:
	temp = [int(k) for k in line[1:]]
	onpeak[line[0]] = temp
csvfile.close()

offpeak = {}
csvfile = file('../peakdate_good_offline.csv', 'r')
reader = csv.reader(csvfile)
for line in reader:
	temp = [int(k) for k in line[1:]]
	offpeak[line[0]] = temp
csvfile.close()

select = list()

namelist = os.listdir('../sep_series/')
fw1 = open('../params_cng_on.csv', 'w')
fw2 = open('../params_cng_off.csv', 'w')
count = 0
for item in namelist:
	if not gooddic.has_key(item[:-4]):
		continue
	csvfile = file('../sep_series/'+item, 'r')
	reader = csv.reader(csvfile)
	data = list()
	for line in reader:
		data.append(line)
	csvfile.close()
	timelist = [int(k) for k in data[0]]
	comelist = [int(k) for k in data[1]]
	golist = [int(k) for k in data[2]]
	onlist = [int(k) for k in data[3]]
	offlist = [int(k) for k in data[4]]
	onqlist = [int(k) for k in data[5]]
	offqlist = [int(k) for k in data[6]]
	t = np.array(timelist)
	c = np.array(comelist)
	g = np.array(golist)
	x = np.array(onlist)
	y = np.array(offlist)
	z = np.array(onqlist)
	w = np.array(offqlist)
	#find begin
	#begin = 0
	#fit online
	params = Parameters()
	params.add('alpha', value=0.3, min=0.0)
	params.add('beta', value=0.05, min=0.0)
	params.add('gamma', value=0.05, min=1.0)

	params.add('G', value=max(2*x[-1],1), min=max(x[-1],1), max=1000000)
	params.add('n', value=x[0], vary=False)
	'''
	m = len(x)
	for i in range(m):
		if x[i] >= 0.01 * x[-1]:
			params.add('n', value=x[i], vary=False)
	'''
	p1 = 0
	if onpeak.has_key(item[:-4]):
		pl = onpeak[item[:-4]]
		p1 = len(pl)
		for i in range(p1):
			params.add('lambdaval'+str(i), value=x[pl[i]]-x[pl[i]-1], min=0, max=x[pl[i]]-x[pl[i]-1]+1)
			params.add('delta'+str(i), value=pl[i], vary=False)
	time = np.array([t, t])
	series = np.array([x, z])
	r1 = minimize(fcn2minMultiImpulse, params, args=(time, series, p1))
	fw1.write(item[:-4]+',')
	fw1.write(str(r1.params))
	fw1.write('\n')
	#fit offline
	params = Parameters()
	params.add('alpha', value=0.3, min=0.0)
	params.add('beta', value=0.05, min=0.0)
	params.add('gamma', value=0.05, min=1.0)
	params.add('G', value=max(2*y[-1],1), min=max(y[-1],1), max=1000000)
	params.add('n', value=y[0], vary=False)
	p2 = 0
	if offpeak.has_key(item[:-4]):
		pl = offpeak[item[:-4]]
		p2 = len(pl)
		for i in range(p2):
			params.add('lambdaval'+str(i), value=y[pl[i]]-y[pl[i]-1], min=0, max=y[pl[i]]-y[pl[i]-1]+1)
			params.add('delta'+str(i), value=pl[i], vary=False)
	time = np.array([t, t])
	series = np.array([y, w])
	r2 = minimize(fcn2minMultiImpulse, params, args=(time, series, p2))
	fw2.write(item[:-4]+',')
	fw2.write(str(r1.params))
	fw2.write('\n')
	nickname = 'Unknown'
	if namedic.has_key(item[:-4]):
		nickname = namedic[item[:-4]]
	namelist.append(item[:-4])
	drawPic(t, x, y, z, w, r1, r2, '../fitpic_comeNgo/'+item[:-4]+'_'+nickname+'.png', p1, p2)
	count += 1
	print count
fw1.close()
fw2.close()

fw = open('../rmse_comeNgo.csv', 'w')
n = len(rmse)
for i in range(n):
	fw.write(namelist[i])
	for j in range(4):
		fw.write(',')
		fw.write(str(rmse[i][j]))
	fw.write('\n')
fw.close()
