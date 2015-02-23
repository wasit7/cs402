import os
import sys
import pickle
from scmaster import master
from sctree import tree
import imp
import numpy as np
from matplotlib import pyplot as plt
import time
import datetime
def timestamp(ti=time.time()):
    tf=time.time()    
    print("    took: %.2f sec"%(tf-ti))
    return tf
def train(dsetname='scdataset_spiral'):
    print("main>>dsetname: {}".format(dsetname))
    #training
    m=master(dsetname)
    
    ts=time.time()
    strtime=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print("Starting time: "+strtime)
    
       
    m.reset()
    print("----main::train::m.reset()")
    ts=timestamp(ts)
    #print("main>>H,Q:".format(m.reset()))
    strtime=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    m.train(strtime)
    print("----main::train::m.trian()") 
    ts=timestamp(ts)
    #recording the tree pickle file
    if not os.path.exists(dsetname):
        os.makedirs(dsetname)
    pickleFile = open(dsetname+'/root.pic', 'wb')
    pickle.dump(m.root, pickleFile, pickle.HIGHEST_PROTOCOL)
    pickleFile.close()

def recall(dsetname='scdataset_spiral'):
    ts=time.time()
    strtime=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print("Starting time: "+strtime)
    
    #reading the tree pickle file
    pickleFile = open(dsetname+'/root.pic', 'rb')
    root = pickle.load(pickleFile)
    pickleFile.close()
    #init the test tree
    t=tree()
    t.settree(root)
    print("----main::recall::loadtree") 
    ts=timestamp(ts)
    
    #compute recall rate
    loader= imp.load_source('dataset', dsetname+'.py')
    dset=loader.dataset()
    correct=0;
    for i in xrange(dset.size):
        if dset.getL(i) == t.getL(dset.I[:,i]):
            correct=correct+1
    print("recall rate: {}%".format(correct/float(dset.size)*100))
    print("----main::recall::evaluate") 
    ts=timestamp(ts)
    return t

def show(dsetname='scdataset_spiral'):
    t=recall(dsetname)
    #setup the new test-set
    d=0.01
    y, x = np.mgrid[slice(-1, 1+d, d), slice(-1, 1+d, d)]
    
    #start labeling
    L=np.zeros(x.shape,dtype=int)
    for r in xrange(x.shape[0]):
        for c in xrange(x.shape[1]):
            L[r,c]=t.getL(np.array([ x[r,c],y[r,c] ]))
    
    #plot the lalbel out put
    plt.close('all')
    plt.axis([-1,1,-1,1])
    plt.pcolor(x,y,L)
    plt.show()
    
    #overlaying new input data
    loader= imp.load_source('dataset', dsetname+'.py')
    dset=loader.dataset()
    
    plt.hold(True)
    marker=['bo','co','go','ro','mo','yo','ko',
            'bs','cs','gs','rs','ms','ys','ks']
    marker_num=np.min((dset.size,500))
    for i in dset.getX()[:marker_num]:
        if dset.samples[0,i]<14:
            mstr=marker[dset.samples[0,i]]
        else:
            mstr='k*'
        plt.plot(dset.I[0,i],dset.I[1,i],mstr)
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage:main.py dsetname [optional: mode]')
        print(">>ipython main.py dsetname")
        train()
        recall()
        show()
    elif len(sys.argv) == 2:
        train(sys.argv[1])
        recall(sys.argv[1])
    elif len(sys.argv) == 3:
        if sys.argv[2]=='show':
            show(sys.argv[1])
        if sys.argv[2]=='profile':
            import cProfile, pstats, StringIO
            pr = cProfile.Profile()
            pr.enable()
            # ... do something ...
            train(sys.argv[1])
            pr.disable()
            s = StringIO.StringIO()
            #sortby = 'cumulative'
            sortby = 'tot'
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
            ps.print_stats(50)
            print s.getvalue()