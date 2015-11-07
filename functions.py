#!/usr/bin/env python

#color setting
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'

#import public module
import sys
import math
import re
import csv
import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import *

#General reactions
class Reactions:
    def __init__(self,time=0):
        self.time = time
        self.sl = []

    def Readseq(self, readseq='sequence.txt'):
        print "------------------------------------------------------------------"
        print "| "+RED+"A whole-genome based simulation of prokaryotic DNA replication"+ENDC+" |"
        print "| "+GREEN+"MODEL : "+YELLOW+"Escherichia coli K-12 substr. MG1655                  "+ENDC+" |"
        print "------------------------------------------------------------------"
        seq = open(readseq)
        self.f = seq.read()
        self.m = []
        for i in range(len(self.f)):
            self.m.append([0,0,0,0,0,0,0,0,0,0,self.f[i],''])
        #ds,dnaA,dnaB,dnaC,dnaG,SSB,Topo1,SDC,DNApol1,DNApol3
        return self.f,self.m,self.time,self.sl

    def Monomer(self,name,num,sublist):
        self.name = str(name)
        self.num = num
        print "{:<20}".format(YELLOW+self.name+ENDC)+" = "+BLUE+`self.num`+ENDC
        gn = [self.name,self.num]
        sublist.append(gn)
        return sublist

    def Complex(self,name,num,complexlist):
        self.name = str(name)
        self.num = num
        print "{:<55}".format(RED+self.name+ENDC)+" = "+BLUE+`self.num`+ENDC
        gn = [self.name,self.num]
        complexlist.append(gn)
        return complexlist

    def Enzyme(self,name,num,enzymelist):
        self.name = str(name)
        self.num = num
        print "{:<55}".format(GREEN+self.name+ENDC)+" = "+BLUE+`self.num`+ENDC
        gn = [self.name,self.num]
        enzymelist.append(gn)
        return enzymelist

    def Region(self,region,state):
        pass

    def Getindex(self, name, sublist):
        for i in range(len(sublist)):
            if sublist[i][0] == name:
                return i

class Compose:
    def __init__(self,name,components,comnum,k):
        self.name = name
        self.components = components
        self.comnum = comnum
        self.k = k

    def propensity(self, state):
        self.p = self.k
        for i in range(len(self.components)):
            self.p = self.p * state[Reactions().Getindex(self.components[i],state)][1]
        return self.p

    def execute(self, state):
        for i in range(len(self.components)):
            state[Reactions().Getindex(self.components[i],state)][1] -= self.comnum[i]
        state[Reactions().Getindex(self.name,state)][1] += 1
        return state

class Decompose:
    def __init__(self,name,components,comnum,k):
        self.name = name
        self.components = components
        self.comnum = comnum
        self.k = k

    def propensity(self, state):
        self.p = self.k * state[Reactions().Getindex(self.name,state)][1]
        return self.p

    def execute(self, state):
        for i in range(len(self.components)):
            state[Reactions().Getindex(self.components[i],state)][1] += self.comnum[i]
        state[Reactions().Getindex(self.name,state)][1] -= 1
        return state

class Showdata:
    def __init__(self):
        pass

    def logger(self, t, sublist, st, et):
        otime = [t]
        data = []
        for i in range(len(sublist)):
            data.append([sublist[i][1]])
        self.data = data
        self.time = otime
        self.st = st
        self.et = et
        return self.time, self.data, self.st, self.et

    def getdata(self, t, sublist, logt, logd):
        for i in range(len(sublist)):
            logd[i].append(sublist[i][1])
        logt.append(t)
        return logt, logd

    def figure(self, name, logt, logd, sublist):
        for i in range(len(sublist)):
            if sublist[i][0] == str(name):
                plt.plot(logt, logd[i][:], label=sublist[i][0])

    def save(self, name="figure.png"):
        plt.legend()
        plt.savefig(name)
        plt.close()

class Simulation:
    def __init__(self):
        pass

    def Step(self, time, state, events):
        atotal = 0
        alist = []
        for i in range(len(events)):
                atotal += events[i].propensity(state)
                alist.append(events[i].propensity(state))
        tau = float((1/atotal)*math.log1p(1/rand()))
        newt = time + tau
        a0, l = 0, 0
        r = rand()*atotal
        print newt
        for a in alist:
            a0 += a
            if a0 > r: j = l
            else: l += 1
        news = events[j].execute(state)
        return newt, news

    def run(self, t, tend, SubList, events, logt, logd):
        while t <= tend:
            t, SubList = Simulation().Step(t, SubList, events)
            logt, logd = Showdata().getdata(t, SubList, logt, logd)
        return t, SubList, logt, logd

    def Wcplot(self, time, data):
        plt.plot(time, data, 'b', label="ERROR BASE")
        plt.xlabel("Time[s]", fontsize=12)
        plt.ylabel("ERROR BASE", fontsize=12)
        plt.title("Error Accumulation", fontsize=14)
        plt.savefig("error.png")
        plt.close()

    def Wcwrite(self, mod):
        result = open('result.txt', 'w')
        for line in mod:
            result.write(str(line)+'\n')
        result.close()

    def Makedata(self, dirname="result"):
        pwd = os.getcwd()
        if os.path.exists(pwd+"/"+dirname):
            swt = 1
            print BLUE+dirname+RED+" already exists !!"+ENDC
            dirname = raw_input(YELLOW+"Please input other name : "+ENDC)
            while swt == 1:
                if os.path.exists(pwd+"/"+dirname):
                    dirname = raw_input(RED+"ERROR "+GREEN+"Please input other name : "+ENDC)
                else: break
        os.mkdir(dirname)
        if os.path.exists(pwd+'/error.png'): shutil.move('error.png',pwd+"/"+dirname)
        if os.path.exists(pwd+'/result.txt'):shutil.move('result.txt',pwd+"/"+dirname)
        if os.path.exists(pwd+'/complex.png'):shutil.move('complex.png',pwd+"/"+dirname)
